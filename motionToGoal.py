from robot_class import Robot
import time as time
import numpy as np
import matplotlib.pyplot as plt

def saturation_function(proportional_speed, max_forward_speed, max_backward_speed, error):
    if proportional_speed < -error:
        if proportional_speed < max_backward_speed:
            return max_backward_speed
        else:
            return proportional_speed + error
    elif proportional_speed > error:
        if proportional_speed > max_forward_speed:
            return max_forward_speed
        else:
            return proportional_speed - error
    else:
        return 0


def main(demonstrating):
    rob = Robot()

    max_forward = rob.encoder.get_max_forward_speed()
    max_backward = rob.encoder.get_max_backward_speed()

    desired_distance = 5
    # Proportional gain
    camera_Kp = 0.01
    sensor_Kp = 1.5

    user_input = input("Place robot in front of wall and press enter to continue.")

    if demonstrating:
        while True:
            distance = rob.distance_sensor.get_front_inches()
            forward_control = saturation_function(sensor_Kp * (distance - desired_distance),
                                                        max_forward, max_backward, 0.2)
            blobs = rob.camera.get_blobs()

            #Find largest blob
            largest = -1
            size = 0.0
            for i in range(len(blobs)):
                if blobs[i].size > size:
                    size = blobs[i].size
                    largest = i

            if len(blobs) > 0:
                sideways_control = saturation_function(camera_Kp * (blobs[largest].pt[0] - 320),
                                                    max_forward, max_backward, 0.05)
                rob.encoder.setSpeedsIPS(min(forward_control + sideways_control, max_forward), 
                                         max(forward_control - sideways_control, max_backward))
            else:
                sideways_control = saturation_function(camera_Kp * 1000, max_forward, max_backward, 0.05)
                rob.encoder.setSpeedsIPS(sideways_control, -sideways_control)

            time.sleep(0.01)
    else:
        start_time = time.monotonic()
        distance_list = []
        x_axis = []
        while time.monotonic() <= (start_time + 30):
            distance = rob.distance_sensor.get_front_inches()
            proportional_control = saturation_function(Kp * (desired_distance - distance),
                                                        max_forward, max_backward)
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
