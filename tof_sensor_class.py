import time
import sys
sys.path.append('/home/pi/VL53L0X_rasp_python/python')
import VL53L0X
import RPi.GPIO as GPIO

class DistanceSensor():
    def __init__(self):

        # Pins that the sensors are connected to
        self.LSHDN = 27
        self.FSHDN = 22
        self.RSHDN = 23

        self.MAX_RANGE_INCHES = 47.24
        self.MAX_RANGE_MM = 1200

        self.DEFAULTADDR = 0x29 # All sensors use this address by default, don't change this
        self.LADDR = 0x2a
        self.RADDR = 0x2b

        # Set the pin numbering scheme to the numbering shown on the robot itself.
        GPIO.setmode(GPIO.BCM)

        # Setup pins
        GPIO.setup(self.LSHDN, GPIO.OUT)
        GPIO.setup(self.FSHDN, GPIO.OUT)
        GPIO.setup(self.RSHDN, GPIO.OUT)

        # Shutdown all sensors
        GPIO.output(self.LSHDN, GPIO.LOW)
        GPIO.output(self.FSHDN, GPIO.LOW)
        GPIO.output(self.RSHDN, GPIO.LOW)

        time.sleep(0.01)

        # Initialize all sensors
        self.lSensor = VL53L0X.VL53L0X(address=self.LADDR)
        self.fSensor = VL53L0X.VL53L0X(address=self.DEFAULTADDR)
        self.rSensor = VL53L0X.VL53L0X(address=self.RADDR)

        # Connect the left sensor and start measurement
        GPIO.output(self.LSHDN, GPIO.HIGH)
        time.sleep(0.01)
        self.lSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

        # Connect the right sensor and start measurement
        GPIO.output(self.RSHDN, GPIO.HIGH)
        time.sleep(0.01)
        self.rSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

        # Connect the front sensor and start measurement
        GPIO.output(self.FSHDN, GPIO.HIGH)
        time.sleep(0.01)
        self.fSensor.start_ranging(VL53L0X.VL53L0X_GOOD_ACCURACY_MODE)

    # Returns sensor input conveted from mm to inches
    def get_front_inches(self):
        f_distance = self.fSensor.get_distance()
        if (f_distance / 25.4) > 40:
            return 40.0
        else:
            return f_distance / 25.4

    def get_left_inches(self):
        l_distance = self.lSensor.get_distance()
        if (l_distance / 25.4) > 35:
            return 35.0
        else:
            return l_distance / 25.4

    def get_right_inches(self):
        r_distance = self.rSensor.get_distance()
        if (r_distance / 25.4) > 40:
            return 40.0
        else:
            return r_distance / 25.4

    def ctrlC(self):
        print("Stopping sensors")
        self.lSensor.stop_ranging()
        self.fSensor.stop_ranging()
        self.rSensor.stop_ranging()
        
if __name__ == "__main__":
    rob = DistanceSensor()
    for x in range(0,100):
        print("{0}cm {1}in".format(rob.lSensor.get_distance(), rob.get_left_inches()))
        