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
        self.camera = Camera()
        self.blob_x = -1000
        signal.signal(signal.SIGINT, self.ctrlC)
        self.GIF = None
        self.no_wall = None
        self.less_than_10 = None
        self.stop_r = None

        self.orientation = 'n'
        self.cell_size = 18
        self.max_front_distance = 13

    def stop(self):
        print("Exiting Robot")
        self.encoder.ctrlC()
        self.camera.ctrlC()
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
        ticks = int(rotations * 32 * 1.1)
        self.encoder.step_count = (0, 0)
        self.encoder.steps_to_move = [ticks, ticks]
        speed = min(self.encoder.get_max_forward_speed(), -self.encoder.get_max_backward_speed())
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
        while self.encoder.steps_to_move[0] != -1:
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

    def forward(self):
        rotations = (self.cell_size / 2) / (self.encoder.WDIAMETER * math.pi)
        ticks = int(rotations * 32 * 1.05)
        self.encoder.step_count = (0, 0)
        self.encoder.steps_to_move = [ticks, ticks]
        next_cell = NextCell(self, (self.distance_sensor.get_left_inches() < self.cell_size),
                                    (self.distance_sensor.get_right_inches() < self.cell_size))
        #print(self.distance_sensor.get_front_inches())

        # if self.distance_sensor.get_right_inches() < (self.mapper.rob.cell_size / 2):
        #     if self.distance_sensor.get_left_inches() < (self.mapper.rob.cell_size / 2):
        #         follow_both(self)
        #     else:
        #         follow_right(self)
        # elif self.distance_sensor.get_left_inches() < (self.mapper.rob.cell_size / 2):
        #     follow_left(self)
        # else:

        if True:
            #input("Enter to WF")
            # self.encoder.setSpeedsIPS(self.encoder.get_max_forward_speed(), self.encoder.get_max_forward_speed())
            # follow_both(self, next_cell.move_to_cell)
            # while next_cell.move_to_cell():
            #     print("moving to cell")
            #     time.sleep(0.1)

            follow_both(self, next_cell, next_cell.move_to_cell)
            self.encoder.step_count = (0, 0)
            self.encoder.steps_to_move = [ticks, ticks]
            follow_both(self, next_cell, next_cell.center_in_cell)
##            self.encoder.setSpeedsIPS(self.encoder.get_max_forward_speed(), self.encoder.get_max_forward_speed())
            #input("Enter to Center")
#             while next_cell.center_in_cell():
#                 #print("Centering in cell")
#                 distance = self.distance_sensor.get_front_inches()
#                 proportional_control = saturation_function(1.5 * ((self.cell_size / 2 ) - distance),
#                                                         self.encoder.get_max_forward_speed(),
#                                                         self.encoder.get_max_backward_speed())
#                 self.encoder.setSpeedsIPS(proportional_control, proportional_control)
#                 time.sleep(0.01)
# ##
##                time.sleep(0.1)
            self.encoder.stop()


#Class used for determining when a robot has moved to the next cell and when it is centered in it
class NextCell:
    def __init__(self, rob, left_wall = False, right_wall = False):
        self.rob = rob
        #self.initial_distance = initial_distance
        self.left_wall_detected = left_wall
        self.right_wall_detected = right_wall

    # used for moving to the next cell
    # returns false if robot should stop
    def move_to_cell(self):
        if self.rob.distance_sensor.get_front_inches() < (self.rob.cell_size / 2):
            #print(self.initial_distane)
            #print(self.rob.distance_sensor.get_front_inches())
            return False
        if self.left_wall_detected:
            if self.rob.distance_sensor.get_left_inches() > self.rob.cell_size:
                # print("left wall not found")
                return False
        else:
            if self.rob.distance_sensor.get_left_inches() < self.rob.cell_size:
                # print("new left wall found")
                return False

        if self.right_wall_detected:
            if self.rob.distance_sensor.get_right_inches() > self.rob.cell_size:
                # print("right wall not found")
                return False
        else:
             if self.rob.distance_sensor.get_right_inches() < self.rob.cell_size:
                 # print("new right wall found")
                 return False
        if self.rob.encoder.steps_to_move[0] == -1:
            # print("encoder ticks -1")
            return False
        # else:
        #     print(self.rob.encoder.step_count[0])
        #     print(self.rob.encoder.steps_to_move[0])
        #     print()
        return True

    # Used for centering robot in a cell
    # returns false if robot should stop
    def center_in_cell(self):
        # print(self.rob.encoder.steps_to_move[0])
        if self.rob.distance_sensor.get_front_inches() < (self.rob.cell_size / 2):
            return False
        if self.rob.encoder.steps_to_move[0] == -1:
            return False

        # reset encoder steps if the wall state changes: robot was not at the edge of the cell, but is now
        if self.left_wall_detected:
            if self.rob.distance_sensor.get_left_inches() > self.rob.cell_size:
                # print("left wall not found")
                self.rob.encoder.step_count = (0, 0)
                self.left_wall_detected = False
        else:
            if self.rob.distance_sensor.get_left_inches() < self.rob.cell_size:
                # print("new left wall found")
                self.rob.encoder.step_count = (0, 0)
                self.left_wall_detected = True

        if self.right_wall_detected:
            if self.rob.distance_sensor.get_right_inches() > self.rob.cell_size:
                # print("right wall not found")
                self.rob.encoder.step_count = (0, 0)
                self.right_wall_detected = False
        else:
             if self.rob.distance_sensor.get_right_inches() < self.rob.cell_size:
                 # print("new right wall found")
                 self.rob.encoder.step_count = (0, 0)
                 self.right_wall_detected = True

        return True


## Main program
if __name__ == "__main__":
    rob=Robot()
    rob.stop()
