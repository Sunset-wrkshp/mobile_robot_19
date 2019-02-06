from encoder_class import Encoder
import matplotlib.pyplot as plt
import time as time
import numpy as np
import math

class Encoder_Task2(Encoder):
    def setSpeeds(self, pulse):
        self.pwm.set_pwm(self.RSERVO, 0, math.floor(pulse / 20 * 4096))
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(pulse / 20 * 4096))

    def task2(self):
        self.stop()
        self.calibrateSpeeds()
        self.stop()
        i = 1.3
        speeds = []

        while i <= 1.7:
            self.setSpeeds(i)
            time.sleep(1)
            i += 0.01
            speeds.append(self.getSpeeds())

        x_axis = np.arange(1.3, 1.7, 0.01)
        plt.plot(x_axis, speeds)
        plt.show()

## Main program
if __name__ == "__main__":
    enc = Encoder_Task2()
    enc.stop()
    enc.task2()
    enc.stop()
