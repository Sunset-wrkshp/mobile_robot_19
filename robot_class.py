from encoder_class import Encoder
from tof_sensor_class import DistanceSensor
from camera_class import Camera
import signal
import math
import time
from wall_following import follow_both, saturation_function

class Robot():
    def __init__(self, skip = False):
        self.encoder = Encoder()
        if skip is False:
            self.encoder.calibrateSpeeds()
        self.distance_sensor = DistanceSensor()
        #self.camera = Camera()
        self.blob_x = -1000
        signal.signal(signal.SIGINT, self.ctrlC)
        self.GIF = None
        self.no_wall = None
        self.less_than_10 = None
        self.stop_r = None

        self.rotation_Kp = 0.5
        self.wall_distance_change = 0.2
        self.dist_threshold = 1
        self.front_adjustment_Kp = 1.5
        self.dist_from_front_wall = 7
        #self.dist_from_side_wall = 7.64
        self.rotation_mult = 1.35
        self.forward_mult = 1.1
        self.wall_following_Kp = 0.5
        self.orientation = 'n'
        self.cell_size = 18
        self.max_front_distance = self.cell_size / 2

    def stop(self):
        print("Exiting Robot")
        self.encoder.ctrlC()
        #self.camera.ctrlC()
        self.distance_sensor.ctrlC()
        exit()

    def ctrlC(self, signum, frame):
        self.stop()

    #getters and setters
    def goal_in_front(self, val = None):
        #goal is in front of the robot
        if val is not None:
            self.GIF = val
       # else:

        return self.GIF

    def no_wall_detected(self, val = None):
        #No wall is in front of the robot within 10 cm
        if val is not None:
            self.no_wall = val
        return self.no_wall

    def less_than_10cm(self, val = None):
        #something is in front of the robot within 10 cm that is not the goal
        if val is not None:
            self.less_than_10 = val
        return self.less_than_10

    def stop_range(self, val = None):
        #robot front is within proper distance +- error of goal
        if val is not None:
            self.stop_r = val
        return self.stop_r

    #from faceGoal.py
    def check_goal_in_front(self):
        print("Checking GIF()")
        #checks if goal is in front within error range
        #sets robot variable accordingly and returns True or False
        blobs = self.camera.get_blobs()

        ERROR = 0.5
        Kp = 0.009

        t_set = []

        #Find largest blob
        largest = -1
        size = 0.0
        for i in range(len(blobs)):
            if blobs[i].size > size:
                size = blobs[i].size
                largest = i

        for x in range (0,20):
            if len(blobs) > 0:
                self.blob_x = blobs[largest].pt[0]
                if ((Kp * (blobs[largest].pt[0] - 320)) > -ERROR) and ((Kp * (blobs[largest].pt[0] - 320)) < ERROR):
                    if ((Kp* (blobs[largest].pt[1] - 240) > -2*ERROR) and ((Kp * (blobs[largest].pt[1] - 240)) < 2*ERROR)):
##                        self.goal_in_front(True)
                        print("GIF True")
                        t_set.append(True)
                    else:
##                        self.goal_in_front(False)
                        print("GIF False because too high")
                        t_set.append(False)
                else:
##                    self.goal_in_front(False)
                    print("GIF False goal center not in error range")
                    t_set.append(False)
            else:
                self.blob_x = 1000
##                self.goal_in_front(False)
                print("GIF False no blobs")
                t_set.append(False)
        if any(t_set):
            self.goal_in_front(True)
            return True
        else:
            self.goal_in_front(False)
            return False

    def check_no_wall_in_front(self):
        f_distance = self.distance_sensor.get_front_inches()
        GIF = self.check_goal_in_front()
        if (GIF):
            if (f_distance > 3*5):
                print("GIF but also a wall")
                self.no_wall_detected(True)
                return True
            else:
                self.no_wall_detected(False)
                return False

    def rotate(self, direction='r'):
        rotations = (self.encoder.WSEPARATION * math.pi / 4) / (self.encoder.WDIAMETER * math.pi)
        ticks = int(rotations * 32 * self.rotation_mult)
        self.encoder.step_count = (0, 0)
        self.encoder.steps_to_move = [ticks, ticks]
        max_forward = self.encoder.get_max_forward_speed()
        max_backward = self.encoder.get_max_backward_speed()
        speed = min(self.encoder.get_max_forward_speed(), -self.encoder.get_max_backward_speed())
        #print(speed)
        if direction.lower() == 'r':
            self.encoder.setSpeedsIPS(speed, -speed)
            if self.orientation == 'n':
                self.orientation = 'e'
            elif self.orientation == 'e':
                self.orientation = 's'
            elif self.orientation == 's':
                self.orientation = 'w'
            else:
                self.orientation = 'n'
        else:
            self.encoder.setSpeedsIPS(-speed, speed)
            if self.orientation == 'n':
                self.orientation = 'w'
            elif self.orientation == 'e':
                self.orientation = 'n'
            elif self.orientation == 's':
                self.orientation = 'e'
            else:
                self.orientation = 's'
        while (self.encoder.steps_to_move[0] != -1) or (self.encoder.steps_to_move[1] != -1):
            proportional_speed = self.rotation_Kp * (self.encoder.steps_to_move[0] - self.encoder.step_count[0])
            proportional_control = self.saturation_function(proportional_speed, max_forward, max_backward)
            if direction.lower() == 'r':
                proportional_control = -proportional_control
            self.encoder.setSpeedsIPS(proportional_control, -proportional_control)
            time.sleep(0.01)
        self.encoder.stop()
        time.sleep(0.1)

    def get_right_dir(self):
        if self.orientation == 'n':
            return 'e'
        elif self.orientation == 'e':
            return 's'
        elif self.orientation == 's':
            return 'w'
        else:
            return 'n'

    def get_left_dir(self):
        if self.orientation == 'n':
            return 'w'
        elif self.orientation == 'w':
            return 's'
        elif self.orientation == 's':
            return 'e'
        else:
            return 'n'

    def change_orientation(self, direction):
        if direction.lower() == 'n':
            if self.orientation == 'n':
                return
            elif self.orientation == 'e':
                self.rotate('l')
            elif self.orientation == 's':
                self.rotate('l')
                self.rotate('l')
            else:
                self.rotate('r')
        elif direction.lower() == 'e':
            if self.orientation == 'e':
                return
            elif self.orientation == 's':
                self.rotate('l')
            elif self.orientation == 'w':
                self.rotate('l')
                self.rotate('l')
            else:
                self.rotate('r')
        elif direction.lower() == 's':
            if self.orientation == 's':
                return
            elif self.orientation == 'w':
                self.rotate('l')
            elif self.orientation == 'n':
                self.rotate('l')
                self.rotate('l')
            else:
                self.rotate('r')
        elif direction.lower() == 'w':
            if self.orientation == 'w':
                return
            elif self.orientation == 'n':
                self.rotate('l')
            elif self.orientation == 'e':
                self.rotate('l')
                self.rotate('l')
            else:
                self.rotate('r')

    #moves robot forward
    #returns whether or not it stopped early
    def forward(self):
        rotations = (self.cell_size / 2) / (self.encoder.WDIAMETER * math.pi)
        ticks = int(rotations * 32 * self.forward_mult)
        self.encoder.step_count = (0, 0)
        self.encoder.steps_to_move = [ticks, ticks]
        next_cell = NextCell(self)
        time.sleep(0.1)

        follow_both(self, next_cell, next_cell.move_to_cell, self.wall_following_Kp, self.dist_from_front_wall)
        self.encoder.stop()
        if self.distance_sensor.get_front_inches() < self.dist_from_front_wall:
            return True
        #user_input = input("moved to cell border")
        self.encoder.step_count = (0, 0)
        self.encoder.steps_to_move = [ticks, ticks]
        next_cell.initialize_walls()
        time.sleep(0.1)
        follow_both(self, next_cell, next_cell.center_in_cell, self.wall_following_Kp, self.dist_from_front_wall)
        self.encoder.stop()
        #user_input = input("Centered in cell")
        if (self.distance_sensor.get_front_inches() < self.max_front_distance) \
                and (abs(self.distance_sensor.get_front_inches() - self.dist_from_front_wall) > self.dist_threshold):
            self.adjust_front_distance()
        if (self.distance_sensor.get_right_inches() < self.cell_size) \
                and abs(self.distance_sensor.get_right_inches() - self.dist_from_front_wall) > self.dist_threshold:
            self.rotate('r')
            self.adjust_front_distance()
            self.rotate('l')
        if (self.distance_sensor.get_left_inches() < self.cell_size) \
                and abs(self.distance_sensor.get_left_inches() - self.dist_from_front_wall) > self.dist_threshold:
            self.rotate('l')
            self.adjust_front_distance()
            self.rotate('r')
        time.sleep(0.1)
        return False

    def adjust_front_distance(self):
        max_forward = self.encoder.get_max_forward_speed() / 2
        max_backward = self.encoder.get_max_backward_speed() / 2
        while abs(self.distance_sensor.get_front_inches() - self.dist_from_front_wall) > self.dist_threshold:
            proportional_speed = self.front_adjustment_Kp * (self.dist_from_front_wall - self.distance_sensor.get_front_inches())
            proportional_control = self.saturation_function(proportional_speed, max_forward, max_backward)
            self.encoder.setSpeedsIPS(proportional_control, proportional_control)
            time.sleep(0.01)
        self.encoder.stop()

    def saturation_function(self, proportional_speed, max_forward_speed, max_backward_speed):
        if proportional_speed > 0.1:
            if -proportional_speed < max_backward_speed:
                return max_backward_speed
            else:
                return -proportional_speed
        elif proportional_speed < -0.1:
            if -proportional_speed > max_forward_speed:
                return max_forward_speed
            else:
                return -proportional_speed
        else:
            return 0


#Class used for determining when a robot has moved to the next cell and when it is centered in it
class NextCell:
    def __init__(self, rob):
        self.rob = rob
        #self.initial_distance = initial_distance
        # self.left_wall_detected = left_wall
        # self.right_wall_detected = right_wall
        self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
        self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
        self.wall_detection_threshold = 0.1
        # self.should_follow_right = True
        # self.should_follow_left = True
        self.wall_samples = 20
        self.initialize_walls()

    def initialize_walls(self):
        num_t = 0
        num_f = 0
        for i in range(self.wall_samples):
            if self.rob.distance_sensor.get_left_inches() < (self.rob.cell_size / 1.5):
                num_t += 1
            else:
                num_f += 1
            # time.sleep(0.01)
        if num_t > num_f:
            self.left_wall_detected = True
        else:
            self.left_wall_detected = False

        num_t = 0
        num_f = 0
        for i in range(self.wall_samples):
            if self.rob.distance_sensor.get_right_inches() < (self.rob.cell_size / 1.5):
                num_t += 1
            else:
                num_f += 1
            # time.sleep(0.01)
        if num_t > num_f:
            self.right_wall_detected = True
        else:
            self.right_wall_detected = False

    # used for moving to the next cell
    # returns false if robot should stop
    def detect_wall_change(self, rdist, ldist):
        if self.rob.distance_sensor.get_front_inches() < self.rob.dist_from_front_wall:
            print("wall change: front wall")
            return True

        # wall not detected -> detected
        #if ((self.prev_right_dist > self.rob.cell_size / 2) and (self.rob.distance_sensor.get_right_inches() < self.rob.cell_size / 2)) \
        #       or ((self.prev_left_dist > self.rob.cell_size / 2) and (self.rob.distance_sensor.get_left_inches() < self.rob.cell_size / 2)):
        if (not self.right_wall_detected) and (self.rob.distance_sensor.get_right_inches() < self.rob.cell_size / 2):
            # self.rob.encoder.stop()
            self.right_wall_detected = True
            print("wall change: right wall detected")
            return True
        if (not self.left_wall_detected) and (self.rob.distance_sensor.get_left_inches() < self.rob.cell_size / 2):
            # self.rob.encoder.stop()
            self.left_wall_detected = True
            print("wall change: left wall detected")
            return True

        # wall detected -> not detected
        #if ((self.prev_right_dist < self.rob.cell_size / 2) and (abs(rdist - self.prev_right_dist) > (rdist * self.rob.wall_distance_change))) \
        #       or ((self.prev_left_dist < self.rob.cell_size / 2) and (abs(ldist - self.prev_left_dist) > (ldist * self.rob.wall_distance_change))):
        if self.right_wall_detected and (abs(rdist - self.prev_right_dist) > (rdist * self.rob.wall_distance_change)):
            # self.rob.encoder.stop()
            # print(self.prev_right_dist)
            # print(rdist)
            self.right_wall_detected = False
            print("wall change: right wall not detected")
            return True
        if self.left_wall_detected and (abs(ldist - self.prev_left_dist) > (ldist * self.rob.wall_distance_change)):
            # self.rob.encoder.stop()
            self.left_wall_detected = False
            print("wall change: left wall not detected")
            return True

        return False

    # Returns whether the robot should stop and whether it should wall-follow
    def move_to_cell(self):
        ldist = self.rob.distance_sensor.get_left_inches()
        rdist = self.rob.distance_sensor.get_right_inches()
        if self.detect_wall_change(rdist, ldist):
            self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
            self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
            print("move wall change")
            return False
        # if (abs(ldist - self.prev_left_dist) > (ldist * self.rob.wall_distance_change)) or \
        #         (abs(rdist - self.prev_right_dist) > (rdist * self.rob.wall_distance_change)):
        #     print("detected wall change on side")
        #     self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
        #     self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
        #     return False

        # if self.left_wall_detected:
        #     if self.rob.distance_sensor.get_left_inches() > self.rob.cell_size:
        #         # print("left wall not found")
        #         return False
        # else:
        #     if self.rob.distance_sensor.get_left_inches() < self.rob.cell_size:
        #         # print("new left wall found")
        #         return False

        # if self.right_wall_detected:
        #     if self.rob.distance_sensor.get_right_inches() > self.rob.cell_size:
        #         # print("right wall not found")
        #         return False
        # else:
        #      if self.rob.distance_sensor.get_right_inches() < self.rob.cell_size:
        #          # print("new right wall found")
        #          return False
        if (self.rob.encoder.steps_to_move[0] == -1) and (self.rob.encoder.steps_to_move[1] == -1):
            self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
            self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
            print("move: encoder ticks -1")
            return False
        # else:
        #     print(self.rob.encoder.step_count[0])
        #     print(self.rob.encoder.steps_to_move[0])
        #     print()
        self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
        self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
        return True

    # Used for centering robot in a cell
    # returns false if robot should stop
    def center_in_cell(self):
        ldist = self.rob.distance_sensor.get_left_inches()
        rdist = self.rob.distance_sensor.get_right_inches()
        # print(self.rob.encoder.steps_to_move[0])
        if self.rob.distance_sensor.get_front_inches() < (self.rob.cell_size / 2):
            self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
            self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
            print("center: front wall")
            return False
        if (self.rob.encoder.steps_to_move[0] == -1) and (self.rob.encoder.steps_to_move[1] == -1):
            print("center: encoder steps -1")
            self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
            self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
            return False

        # reset encoder steps if the wall state changes: robot was not at the edge of the cell, but is now
        if self.detect_wall_change(rdist, ldist):
            print("center wall change")
            self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
            self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
            self.rob.encoder.step_count = (0,0)
        # if self.left_wall_detected:
        #     if self.rob.distance_sensor.get_left_inches() > self.rob.cell_size:
        #         # print("left wall not found")
        #         self.rob.encoder.step_count = (0, 0)
        #         self.left_wall_detected = False
        # else:
        #     if self.rob.distance_sensor.get_left_inches() < self.rob.cell_size:
        #         # print("new left wall found")
        #         self.rob.encoder.step_count = (0, 0)
        #         self.left_wall_detected = True
        #
        # if self.right_wall_detected:
        #     if self.rob.distance_sensor.get_right_inches() > self.rob.cell_size:
        #         # print("right wall not found")
        #         self.rob.encoder.step_count = (0, 0)
        #         self.right_wall_detected = False
        # else:
        #      if self.rob.distance_sensor.get_right_inches() < self.rob.cell_size:
        #          # print("new right wall found")
        #          self.rob.encoder.step_count = (0, 0)
        #          self.right_wall_detected = True

        self.prev_right_dist = self.rob.distance_sensor.get_right_inches()
        self.prev_left_dist = self.rob.distance_sensor.get_left_inches()
        return True


## Main program
if __name__ == "__main__":
    rob=Robot()
    rob.stop()
