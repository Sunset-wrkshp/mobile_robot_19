from encoder_class import Encoder
import math
import time as time

class Forward_Encoder(Encoder):
    ticks_left_R = 0
    ticks_left_L = 0
    calibrating = False

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self , pin):
        if (self.ticks_left_L > 0) and (self.calibrating == False):
            self.ticks_left_L -= 1
        elif self.calibrating == False:
            self.pwm.set_pwm(self.LSERVO, 0, 0)
        # print("Left encoder ticked!")
        self.step_count = (self.step_count[0]+1, self.step_count[1])
        # Record the time when the encoders are ticked
        self.prev_tick_time[0] = self.last_tick_time[0]
        self.last_tick_time[0] = time.monotonic()

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        if (self.ticks_left_R > 0) and (self.calibrating == False):
            self.ticks_left_R -= 1
        elif self.calibrating == False:
            self.pwm.set_pwm(self.RSERVO, 0, 0)
        # print("Right encoder ticked!")
        # global step_count
        self.step_count = (self.step_count[0], self.step_count[1]+1)
        self.prev_tick_time[1] = self.last_tick_time[1]
        self.last_tick_time[1] = time.monotonic()

## Main program
if __name__ == "__main__":
    robot = Forward_Encoder()
    robot.stop()
    robot.calibrating = True
    robot.calibrateSpeeds()
    robot.calibrating = False
    robot.stop()
    
    loop = "Y"
    while (loop == "Y"):
        dist = float(input("input distance in inches: "))
        num_seconds = float(input("input time in seconds: "))
        # rotations = distance / wheel circumference
        rotations = dist / (robot.WDIAMETER*math.pi)

        if num_seconds <= 0:
            print("Time must be positive")
        elif dist < 0:
            print("Distance must be positive")
        elif ((rotations / num_seconds > robot.calibrated_speeds[0][1]) or 
                (rotations / num_seconds > robot.calibrated_speeds[-1][0])):
            print("Cannot travel " + str(dist) + " inches in " + str(num_seconds) + " seconds.")
        elif dist > 0:
            robot.ticks_left_L = int(rotations * 32)
            robot.ticks_left_R = int(rotations * 32)

            robot.setSpeedsRPS(rotations / num_seconds, rotations / num_seconds)

            loop = input("Please wait for the robot to finish. Enter 'Y' to continue: ")
            
            while (robot.ticks_left_R > 0) or (robot.ticks_left_L > 0):
                loop = input("Please wait for the robot to finish. Enter 'Y' to continue: ")
            loop = loop.upper()