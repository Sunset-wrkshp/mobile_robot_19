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
        self.less_than_10cm = None
        self.stop_range = None

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
            self.less_than_10cm = val
        return self.less_than_10cm

    def stop_range(self, val = None):
        #robot front is within proper distance +- error of goal
        if val is not None:
            self.stop_range = val
        return self.stop_range

    #from faceGoal.py
    def check_goal_in_front(self):
        #checks if goal is in front within error range
        #sets robot variable accordingly and returns True or False
        blobs = self.camera.get_blobs()

        ERROR = 0.2
        Kp = 0.01

        #Find largest blob
        largest = -1
        size = 0.0
        for i in range(len(blobs)):
            if blobs[i].size > size:
                size = blobs[i].size
                largest = i

        if ((Kp * (blobs[largest].pt[0] - 320)) > -error) and ((Kp * (blobs[largest].pt[0] - 320)) < error):
            self.goal_in_front(True)
            return True
        else:
            self.goal_in_front(False)
            return False
