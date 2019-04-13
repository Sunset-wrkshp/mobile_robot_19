from robot_class import Robot
import time as time
import numpy as np
import matplotlib.pyplot as plt

def saturation_function(proportional_speed, max_forward_speed, max_backward_speed):
    if proportional_speed > 0.1:
        if -proportional_speed < max_backward_speed:
            return max_backward_speed
        else:
            return -proportional_speed
    elif proportional_speed < -0.1:
        if -proportional_speed > max_forward_speed:
            return max_forward_speed
        else:
            return -proportional_speed
    else:
        return 0


def main(demonstrating):
    rob = Robot()

    desired_distance = 9
    # Proportional gain
    Kp = 1.5

    user_input = input("Place robot in front of wall and press enter to continue.")

    if demonstrating:
        while True:
            distance = rob.distance_sensor.get_front_inches()
            proportional_control = saturation_function(Kp * (desired_distance - distance),
                                                        rob.encoder.get_max_forward_speed(),
                                                        rob.encoder.get_max_backward_speed())
            rob.encoder.setSpeedsIPS(proportional_control, proportional_control)
            time.sleep(0.01)
    else:
        start_time = time.monotonic()
        distance_list = []
        x_axis = []
        while time.monotonic() <= (start_time + 30):
            distance = rob.distance_sensor.get_front_inches()
            proportional_control = saturation_function(Kp * (desired_distance - distance),
                                                        rob.encoder.get_max_forward_speed(),
                                                        rob.encoder.get_max_backward_speed())
            rob.encoder.setSpeedsIPS(proportional_control, proportional_control)
            distance_list.append(distance)
            time.sleep(0.01)
            x_axis.append(time.monotonic() - start_time)

        plt.plot(x_axis, distance_list)
        plt.suptitle("Distance from wall over 30s with Kp ={0}".format(Kp))
        plt.ylabel("Distance (inches)")
        plt.xlabel("Time (seconds)")
        plt.show()

## Main program
if __name__ == "__main__":
    main(True)
