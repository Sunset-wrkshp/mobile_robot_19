from robot_class import Robot
import time as time

def saturation_function(proportional_speed, max_forward_speed, max_backward_speed):
    if proportional_speed > 0.1:
        if proportional_speed < max_backward_speed:
            return max_backward_speed
        else:
            return proportional_speed
    elif proportional_speed < -0.1:
        if proportional_speed > max_forward_speed:
            return max_forward_speed
        else:
            return proportional_speed
    else:
        return 0

rob = Robot()
max_forward = rob.encoder.get_max_forward_speed()
max_backward = rob.encoder.get_max_backward_speed()

desired_distance = 5
# Proportional gain
Kp = 0.01
    
user_input = input("Place robot facing goal and press enter to continue.")

while (True):
    blobs = rob.camera.get_blobs()
    
    #Find largest blob
    largest = -1
    size = 0.0
    for i in range(len(blobs)):
        if blobs[i].size > size:
            size = blobs[i].size
            largest = i

    if len(blobs) > 0:
        proportional_control = saturation_function(Kp * (blobs[i].pt[0] - 320),
                                                    max_forward, max_backward)
    else:
        proportional_control = saturation_function(Kp * 640, max_forward, max_backward)
    
    rob.encoder.setSpeedsIPS(proportional_control, -proportional_control)
    time.sleep(0.01)