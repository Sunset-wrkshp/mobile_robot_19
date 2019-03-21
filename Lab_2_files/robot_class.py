from encoder_class import Encoder
from tof_sensor_class import DistanceSensor

class Robot():
    def __init__(self):
        self.encoder = Encoder()
        self.encoder.calibrateSpeeds()
        self.distance_sensor = DistanceSensor()
