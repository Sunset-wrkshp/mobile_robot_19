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
        if val is not None:
            self.GIF = val
        return self.GIF

    def no_wall_detected(self, val = None):
        if val is not None:
            self.no_wall = val
        return self.no_wall

    def less_than_10cm(self, val = None):
        if val is not None:
            self.less_than_10cm = val
        return self.less_than_10cm

    def stop_range(self, val = None):
        if val is not None:
            self.stop_range = val
        return self.stop_range

