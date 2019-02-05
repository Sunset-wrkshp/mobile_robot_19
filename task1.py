from encoder_class import Encoder
import matplotlib.pyplot as plt
import time as time
import numpy as np

class Encoder_Task1(Encoder):
    def setSpeeds(self, Lspeed, Rspeed):
        self.setSpeedsRPS(Lspeed / 60.0, Rspeed / 60.0)

    def task1(self):
        self.calibrateSpeeds()
        self.setSpeeds(0, 10)
        time.sleep(1)
        speeds = []

        for i in range(334):
            speeds.append(self.getSpeeds()[1])
            time.sleep(0.03)

        x_axis = np.arange(0.0, 10.02, 0.03)
        plt.plot(x_axis, speeds)
        plt.show()
        self.stop()

## Main program
if __name__ == "__main__":
    enc = Encoder_Task1()
    enc.stop()
    enc.task1()
    enc.stop()
