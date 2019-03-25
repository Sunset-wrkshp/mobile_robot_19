from encoder_class import Encoder
from tof_sensor_class import DistanceSensor
from camera_class import Camera
import signal

class Robot():
    def __init__(self):
        self.encoder = Encoder()
        self.encoder.calibrateSpeeds()
        self.distance_sensor = DistanceSensor()
        self.camera = Camera()
        signal.signal(signal.SIGINT, self.ctrlC)
        self.GIF = None
        self.no_wall = None
        self.less_than_10 = None
        self.stop_r = None

    def stop(self):
        print("Exiting")
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
        print("Checking")
        #checks if goal is in front within error range
        #sets robot variable accordingly and returns True or False
        blobs = self.camera.get_blobs()

        ERROR = 0.5
        Kp = 0.009

        #Find largest blob
        largest = -1
        size = 0.0
        for i in range(len(blobs)):
            if blobs[i].size > size:
                size = blobs[i].size
                largest = i

        if len(blobs) > 0:
            if ((Kp * (blobs[largest].pt[0] - 320)) > -ERROR) and ((Kp * (blobs[largest].pt[0] - 320)) < ERROR):
                if ((Kp* (blobs[largest].pt[1] - 240) > -2*ERROR) and ((Kp * (blobs[largest].pt[1] - 240)) < 2*ERROR)):
                    self.goal_in_front(True)
                    print("GIF True")
                    return True
                else:
                    self.goal_in_front(False)
                    print("GIF False because too high")
                    return False
            else:
                self.goal_in_front(False)
                print("GIF False goal not in range")
                return False
        else:
            self.goal_in_front(False)
            print("GIF False no blobs")
            return False

    def check_no_wall_in_front(self):
        f_distance = self.distance_sensor.get_front_inches()
        GIF = self.check_goal_in_front()
        if (not GIF):
            print("Goal not in front ")
            if (f_distance > 3*(10*0.393701)):
                print("Nothing within range")
                self.no_wall_detected(True)
                return True
            else:
                print("something within range")
                self.no_wall_detected(False)
                return False
        else:
            print("Goal in front")
            self.no_wall_detected(True)
            return True
