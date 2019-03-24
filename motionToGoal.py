from robot_class import Robot
import time as time
import numpy as np
import matplotlib.pyplot as plt
from faceGoal import faceGoal

def motionToGoal(state_machine, rob):
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

    max_forward = rob.encoder.get_max_forward_speed()
    max_backward = rob.encoder.get_max_backward_speed()

    desired_distance = (10*0.393701)
    # Proportional gain
    camera_Kp = 0.01
    sensor_Kp = 1.5

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
            rob.goal_in_front(True)
            sideways_control = saturation_function(camera_Kp * (blobs[largest].pt[0] - 320),
                                                   max_forward, max_backward, 0.05)
        else:
            rob.goal_in_front(False)
            faceGoal(True, rob)
            continue

        if (forward_control == 0) and (sideways_control == 0):
            #something is within 10 cm in front of robot.
            if state_machine:
                # rob.stop_range(True)
                # rob.goal_in_front(True)
                # rob.no_wall_detected(False)
                rob.less_than_10cm(True)
                return
            else:
                time.sleep(0.1)
        else:
            #goal in front = True?
            rob.encoder.setSpeedsIPS(min(forward_control + sideways_control, max_forward),
                                     max(forward_control - sideways_control, max_backward))

        time.sleep(0.01)

## Main program
if __name__ == "__main__":
    rob = Robot()
    user_input = input("Press enter to continue.")
    motionToGoal(False, rob)
