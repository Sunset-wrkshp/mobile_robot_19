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

    def stop(self):
        print("Exiting")
        self.encoder.ctrlC()
        self.camera.ctrlC()
        self.distance_sensor.ctrlC()
        exit()
        
    def ctrlC(self, signum, frame):
        self.stop()