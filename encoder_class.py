# encoder_class.py
# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.

import time
import RPi.GPIO as GPIO
import signal

class Encoder():
    step_count = ()
    LENCODER = 17
    RENCODER = 18
    calibrated_inputs = [1.4, 1.7]
    calibrated_speeds = []

    def __init__(self):
        self.step_count = (0,0)
        # Attach the Ctrl+C signal interrupt
        signal.signal(signal.SIGINT, self.ctrlC)

        # Set the pin numbering scheme to the numbering shown on the robot itself.
        GPIO.setmode(GPIO.BCM)

        # Set encoder pins as input
        # Also enable pull-up resistors on the encoder pins
        # This ensures a clean 0V and 3.3V is always outputted from the encoders.
        GPIO.setup(self.LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Attach a rising edge interrupt to the encoder pins
        GPIO.add_event_detect(self.LENCODER, GPIO.RISING, self.onLeftEncode)
        GPIO.add_event_detect(self.RENCODER, GPIO.RISING, self.onRightEncode)

    # Pins that the encoders are connected to


    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self , pin):
        print("Left encoder ticked!")
        self.step_count = (self.step_count[0]+1, self.step_count[1])

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        print("Right encoder ticked!")
        # global step_count
        self.step_count = (self.step_count[0], self.step_count[1]+1)

    # This function is called when Ctrl+C is pressed.
    # It's intended for properly exiting the program.
    def ctrlC(self, signum, frame):
        print("Exiting")
        GPIO.cleanup()
        exit()

    # Initalizes Encoders
    # Is this needed?
    def initEncoders(self):
        self.step_count = (0,0)

    def resetCounts(self):
        self.step_count = (0,0)

    # Returns left and right ticks from the encoders
    # (left count, right count)
    def getCounts(self):
        print(self.step_count)
    # returns speed of left and right wheels
    # (left speed, right speed)
    def getSpeeds(self):
        time_1 = time.monotonic()
        count_1 = self.step_counts
        
        time.sleep(0.32)        
        
        time_change = time.monotonic() - time_1
        count_change = self.step_counts - count_1
        speeds = []
                
        for i in range(2):
            if (count_change[i] <= 0):
                speeds.append(0)
            else:
                speeds.append(count_change[i] / (time_change * 32.0))   
        return tuple(speeds)

    # Creates a mapping from the servo input to the wheel speed
    def calibrateSpeeds(self):
        for i in self.calibrated_inputs:
            pwm.set_pwm(RSERVO, 0, math.floor(i / 20 * 4096))
            pwm.set_pwm(LSERVO, 0, math.floor(i / 20 * 4096))
            calibrated_speeds[i] = self.getSpeeds()
        pwm.set_pwm(RSERVO, 0, 0)
        pwm.set_pwm(LSERVO, 0, 0)

## Main program
if __name__ == "__main__":
    d = Encoder()
    while True:
        time.sleep(1)
        d.getCounts()
