from encoder_class import Encoder
import math
import time as time

class SShape_Encoder(Encoder):
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
    robot = SShape_Encoder()
    robot.stop()
    robot.calibrating = True
    robot.calibrateSpeeds()
    #robot.calibrating = False
    robot.stop()

    robot.setSpeedsvw(1, math.pi)
    time.sleep(10)
    robot.stop()
    time.sleep(1)
    robot.setSpeedsvw(-1, math.pi)
    time.sleep(10)
    robot.stop()
"""
    R1 = float(input("input R1: "))
    R2 = float(input("input R2: "))
    num_seconds = float(input("input time in seconds: "))

    # rotations = distance / wheel circumference
    # rotations = ((R1+R2) * math.pi) / (2.5*math.pi)
    rotations = (R1 + R2) / 2.5

    if num_seconds <= 0:
        print("Time must be positive")
    elif (R1 < 0) or (R2 < 0):
        print("R1 and R2 must be non-negative")
    elif ((rotations / num_seconds > robot.calibrated_speeds[0][1]) or
            (rotations / num_seconds > robot.calibrated_speeds[-1][0])):
        print("Cannot travel " + str(((R1 + R2) * math.pi)) + " inches in " + str(num_seconds) + " seconds.")
    else:
        # Split the time evenly so that the robot is traveling at close to a constant speed
        num_seconds_R1 = (R1 / (R1 + R2)) * num_seconds
        num_seconds_R2 = (R2 / (R1 + R2)) * num_seconds

        # 1/2 distance between wheels = 1.975
        right_rotations_R1 = (R1 - 1.975) / 2.5
        left_rotations_R1 = (R1 + 1.975) / 2.5
        right_rotations_R2 = (R2 + 1.975) / 2.5
        left_rotations_R2 = (R2 - 1.975) / 2.5

        robot.ticks_left_R = int(left_rotations_R1 * 32)
        robot.ticks_left_L = int(right_rotations_R1 * 32)

        robot.setSpeedsvw((-R1 * math.pi) / num_seconds_R1, math.pi / num_seconds_R1)

        input("Please wait for the robot to finish R1, then press enter")

        while (robot.ticks_left_R > 0) or (robot.ticks_left_L > 0):
            input("Please wait for the robot to finish")

        robot.ticks_left_R = int(left_rotations_R2 * 32)
        robot.ticks_left_L = int(right_rotations_R2 * 32)

        robot.setSpeedsvw((R2 * math.pi) / num_seconds_R2, math.pi / num_seconds_R2)
"""
