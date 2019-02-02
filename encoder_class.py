# encoder_class.py
# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.

import time
import RPi.GPIO as GPIO
import signal
import Adafruit_PCA9685
import math

class Encoder():
    step_count = ()
    LENCODER = 17
    RENCODER = 18
    calibrated_inputs = [1.4,1.425,1.45,1.475,1.5,1.525,1.55,1.575,1.6]
    calibrated_speeds = []
    last_tick_time = [time.monotonic(), time.monotonic()]
    prev_tick_time = [time.monotonic(), time.monotonic()]

    # The servo hat uses its own numbering scheme within the Adafruit library.
    # 0 represents the first servo, 1 for the second, and so on.
    LSERVO = 0
    RSERVO = 1
    pwm = None

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

        # Initialize the servo hat library.
        self.pwm = Adafruit_PCA9685.PCA9685()

        # 50Hz is used for the frequency of the servos.
        self.pwm.set_pwm_freq(50)

    # Pins that the encoders are connected to


    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self , pin):
        # print("Left encoder ticked!")
        self.step_count = (self.step_count[0]+1, self.step_count[1])
        # Record the time when the encoders are ticked
        self.prev_tick_time[0] = self.last_tick_time[0]
        self.last_tick_time[0] = time.monotonic()

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        # print("Right encoder ticked!")
        # global step_count
        self.step_count = (self.step_count[0], self.step_count[1]+1)
        self.prev_tick_time[1] = self.last_tick_time[1]
        self.last_tick_time[1] = time.monotonic()

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

    # returns revolutions per second of left and right wheels
    # (left rps, right rps)
    def getSpeeds(self):
        speeds = []
        current_time = time.monotonic()
        if (current_time - self.last_tick_time[0] > 1):
            speeds.append(0)
        else:
            speeds.append(min(1 / ((current_time - self.last_tick_time[0]) * 32.0),
                              1 / ((self.last_tick_time[0] - self.prev_tick_time[0]) * 32.0)))


        if (current_time - self.last_tick_time[1] > 1):
            speeds.append(0)
        else:
            speeds.append(min(1 / ((current_time - self.last_tick_time[1]) * 32.0),
                              1 / ((self.last_tick_time[1] - self.prev_tick_time[1]) * 32.0)))


        return tuple(speeds)

    # Creates a mapping from the servo input to the wheel speed
    def calibrateSpeeds(self):
        speeds = []
        for i in self.calibrated_inputs:
            self.pwm.set_pwm(self.RSERVO, 0, math.floor(i / 20 * 4096))
            self.pwm.set_pwm(self.LSERVO, 0, math.floor(i / 20 * 4096))
            time.sleep(2)
            measured_speed = self.getSpeeds()
            if (i < 1.5):
                speeds.append((-measured_speed[0], measured_speed[1]))
            else:
                speeds.append((measured_speed[0], -measured_speed[1]))
        self.pwm.set_pwm(self.RSERVO, 0, 0)
        self.pwm.set_pwm(self.LSERVO, 0, 0)
        self.calibrated_speeds = speeds


    def setSpeedsRPS(self, L, R):
        l_i = self.find_index(L, self.calibrated_speeds, 0)
        r_i = self.find_index(R, self.calibrated_speeds, 1)
        print(self.calibrated_inputs[l_i])
        print(self.calibrated_speeds[l_i])
        print(self.calibrated_inputs[r_i])
        print(self.calibrated_speeds[r_i])
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(self.calibrated_inputs[l_i] / 20 * 4096));
        self.pwm.set_pwm(self.RSERVO, 0, math.floor(self.calibrated_inputs[r_i] / 20 * 4096));



    #linear search, returns closest index
    # 0 for ascending list, 1 for descending list
    def find_index(self, num, data, dir):
          i = 0
          last = 0
          cur = 0
          if dir == 0:
            while(i < len(data)):
              if data[i][0] == num:
                  return i
              elif data[i][0] < num:
                  last = i
                  i+=1
              elif data[i][0] > num:
                  last = i-1
                  cur = i
                  if (abs(num - data[last][0]) < abs(num - data[cur][0])):
                      return last
                  else:
                      return cur
          else:
            while(i < len(data)):
                if data[i][1] == num:
                    return i
                elif data[i][1] > num:
                    last = i
                    i+=1
                elif data[i][1] < num:
                    last = i-1
                    cur = i
                    if (abs(num - data[last][1]) < abs(num - data[cur][1])):
                        return last
                    else:
                        return cur




    # Set speed based on velocity v and angular velocity w
"""
    def setSpeedsvw(self, v, w):
        R = v / w
        d_mid = 3.95 / 2
        # VL = w (R+dmid)
        # VR = w (R-dmid)
        setSpeedsIPS(w * (R + d_mid), w * (R - d_mid))
"""
## Main program
if __name__ == "__main__":

    d = Encoder()
    while(1):
        time.sleep(1)
        # d.getCounts()
        d.calibrateSpeeds()
        print(d.calibrated_speeds)

        time.sleep(5)
        print("set speed")
        d.setSpeedsRPS(.4,.4)
        time.sleep(3)
        d.setSpeedsRPS(0,0)
        break

        # d.getSpeeds()
