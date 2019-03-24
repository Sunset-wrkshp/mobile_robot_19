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
    ERROR = 0.5

    desired_distance = 5
    # Proportional gain
    Kp = 0.009

    while (True):
        blobs = rob.camera.get_blobs()

        #Find largest blob
        largest = -1
        size = 0.0
        for i in range(len(blobs)):
            if blobs[i].size > size:
                size = blobs[i].size
                largest = i

        speed = 0
        if len(blobs) > 0:
            if (blobs[largest].pt[0] - 320) < -ERROR:
                speed = Kp * (blobs[largest].pt[0] - 320 + ERROR)
            elif (blobs[largest].pt[0] - 320) > ERROR:
                speed = Kp * (blobs[largest].pt[0] - 320 - ERROR)
            proportional_control = saturation_function(speed, max_forward, max_backward, ERROR)
            #proportional_control = saturation_function(Kp * (blobs[largest].pt[0] - 320),
            #                                            max_forward, max_backward, ERROR)
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

def check_goal_in_front(rob):
    #checks if goal is in front within error range
    #sets robot variable accordingly and returns True or False
    blobs = rob.camera.get_blobs()

    ERROR = 0.2
    Kp = 0.01

    #Find largest blob
    largest = -1
    size = 0.0
    for i in range(len(blobs)):
        if blobs[i].size > size:
            size = blobs[i].size
            largest = i

    if ((Kp * (blobs[largest].pt[0] - 320)) > -error) and ((Kp * (blobs[largest].pt[0] - 320)) < error):
        rob.goal_in_front(True)
        return True
    else:
        rob.goal_in_front(False)
        return False

if __name__ == "__main__":
    rob = Robot()
    user_input = input("Press enter to continue.")
    faceGoal(False, rob)
