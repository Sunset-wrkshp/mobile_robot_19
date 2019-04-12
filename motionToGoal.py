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

    desired_distance = 5
    # Proportional gain
    camera_Kp = 0.025
    sensor_Kp = 2

    while True:
##        print("loop")
        distance = rob.distance_sensor.get_front_inches()
        forward_control = saturation_function(sensor_Kp * (distance - desired_distance),
                                                        max_forward, max_backward, .2)
        blobs = rob.camera.get_blobs()

        #Find largest blob
        largest = -1
        size = 0.0
        for i in range(len(blobs)):
            if blobs[i].size > size:
                size = blobs[i].size
                largest = i

        if len(blobs) > 0:
            print("I found the goal")
            rob.goal_in_front(True)
            sideways_control = saturation_function(camera_Kp * (blobs[largest].pt[0] - 320),
                                                   max_forward, max_backward, .2)
        else:
            print("I'm looking for the goal")
            if(not state_machine):
                faceGoal(True, rob)
                sideways_control = saturation_function(camera_Kp * 640,
                                                   max_forward, max_backward, .2)
            else:
                rob.goal_in_front(False)
                return
##            faceGoal(True, rob)
##            continue

        if (forward_control == 0):
            print("Front not moving")
            if (sideways_control == 0):
                print("side not moving")
                #something is within 10 cm in front of robot.
                if state_machine:
                    # rob.stop_range(True)
                    # rob.goal_in_front(True)
                    # rob.no_wall_detected(False)
                    # print("I'm in the state machine and I'm not moving")
                    # rob.less_than_10cm(True)
                    rob.stop_range(True)
                    return
                else:
                    time.sleep(0.1)
            else:
                continue
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
