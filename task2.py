from encoder_class import Encoder
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time as time
import numpy as np
import math

class Encoder_Task2(Encoder):
    def setSpeeds(self, pulse):
        self.pwm.set_pwm(self.RSERVO, 0, math.floor(pulse / 20 * 4096))
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(pulse / 20 * 4096))

    def task2(self):
        self.stop()
        #self.calibrateSpeeds()
        self.stop()
        speeds = []

        # Starting at 1.3, measure the speed for pwm = i up to 1.7 in
        #   increments of 0.01
        i = 1.3
        while i <= 1.7:
            self.setSpeeds(i)
            last_count = self.step_count
            last_time = time.monotonic()
            time.sleep(1)
            i += 0.01

            if i < 1.5:
                speeds.append((-(self.step_count[0] - last_count[0])/
                                ((time.monotonic() - last_time) * 32.0),
                                (self.step_count[1] - last_count[1])/
                                ((time.monotonic() - last_time) * 32.0)))
            else:
                speeds.append(((self.step_count[0] - last_count[0])/
                                ((time.monotonic() - last_time)*32.0),
                                -(self.step_count[1] - last_count[1])/
                                ((time.monotonic() - last_time) * 32.0)))
            """
            speeds.append(((self.step_count[0] - last_count[0])/
                            ((time.monotonic() - last_time) * 32.0),
                            (self.step_count[1] - last_count[1])/
                            ((time.monotonic() - last_time) * 32.0)))
            """

        self.stop()

        # Construct and show graph
        x_axis = np.arange(1.3, 1.7, 0.01)
        plt.plot(x_axis, speeds, 'x', x_axis, speeds, '-')
        plt.suptitle("Wheel Speed from 1.3 ms to 1.7 ms")
        plt.ylabel("Measured Speed (RPS)")
        plt.xlabel("Pulse Width (ms)")
        left_handle = mpatches.Patch(color='blue', label='Left wheel')
        right_handle = mpatches.Patch(color='orange', label='Right wheel')
        plt.legend(handles=[left_handle, right_handle])
        plt.show()

## Main program
if __name__ == "__main__":
    enc = Encoder_Task2()
    enc.stop()
    enc.task2()
    enc.stop()
