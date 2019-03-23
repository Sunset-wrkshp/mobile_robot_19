from robot_class import Robot
import time as time

def faceGoal(state_machine, rob):
    def saturation_function(proportional_speed, max_forward_speed, max_backward_speed, error):
        if proportional_speed < -error:
       	    if proportional_speed < max_backward_speed:
                return max_backward_speed
            else:
                return proportional_speed
        elif proportional_speed > error:
            if proportional_speed > max_forward_speed:
                return max_forward_speed
            else:
                return proportional_speed
        else:
            return 0

    max_forward = rob.encoder.get_max_forward_speed()
    max_backward = rob.encoder.get_max_backward_speed()
    ERROR = 0.2

    desired_distance = 5
    # Proportional gain
    Kp = 0.01

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
            proportional_control = saturation_function(Kp * (blobs[largest].pt[0] - 320),
                                                        max_forward, max_backward, ERROR)
        else:
            proportional_control = saturation_function(Kp * 640, max_forward, max_backward, ERROR)

        # exit if used in a state machine and error is within acceptable range
        if state_machine and (proportional_control == 0):
            return
        elif (proportional_control == 0):
            time.sleep(0.1)
        else:
            rob.encoder.setSpeedsIPS(proportional_control, -proportional_control)

        time.sleep(0.01)

if __name__ == "__main__":
    rob = Robot()
    user_input = input("Press enter to continue.")
    faceGoal(False, rob)
