from encoder_class import Encoder
from tof_sensor_class import DistanceSensor
from camera_class import Camera
import signal

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

## Main program
if __name__ == "__main__":
    rob=Robot()
    rob.stop()
    