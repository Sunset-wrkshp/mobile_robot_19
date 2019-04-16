#from robot_class import Robot
import time as time

def follow_right(state_machine, rob, wall_dist=7.64):
##    print("following right")
    max_forward = rob.encoder.get_max_forward_speed()
    max_backward = rob.encoder.get_max_backward_speed()

    desired_distance = wall_dist
    # Proportional gain
    Kp = 0.2

##    user_input = input("Place robot beside wall and press enter to continue.")


    r_distance = rob.distance_sensor.get_right_inches()
    f_distance = rob.distance_sensor.get_front_inches()

    if (state_machine and (f_distance >= (desired_distance))):
        rob.check_goal_in_front()
        if (rob.blob_x < 320):
            #check if goal in front
            #check if no wall in front
            print("Goal is in front and getting close to it.")
            rob.goal_in_front(True)
##                rob.no_wall_detected(True)
            rob.encoder.setSpeedsIPS(0,0)
            return

    r_proportional_control = saturation_function(Kp * (desired_distance - r_distance),
                                                    max_forward, max_backward)
    f_proportional_control = saturation_function(Kp * (desired_distance - min(f_distance, r_distance)),
                                                    max_forward, max_backward)

    if (f_distance < 0):
##    if f_distance < (desired_distance * 2):
        #front wall is deteced withing distance*2 inches. Starts to turn
        # print("Turning")
        # rob.encoder.setSpeedsIPS(min(max_forward + r_proportional_control, f_proportional_control,
        #                             max_forward), max_forward)
        return min(max_forward + r_proportional_control, f_proportional_control, max_forward), max_forward
    else:
        if (state_machine and (r_distance > (desired_distance * 20))):
            print("going straight")
            rob.encoder.setSpeedsIPS(max_forward,
                                    max_forward)
        else:
            #No front wall detected
##            print("WF\n l_distance:{0}, l_speed:{1}\nr_distance:{2} r_speed:{3}".format(r_distance,
##                                                                                        min(max_forward - r_proportional_control, max_forward),
##                                                                                        rob.distance_sensor.get_left_inches(),
##                                                                                        min(max_forward + r_proportional_control, max_forward)))
##            print("Wall following")
            # rob.encoder.setSpeedsIPS(min(max_forward + r_proportional_control, max_forward),
            #                         min(max_forward - r_proportional_control, max_forward))
            return min(max_forward + r_proportional_control, max_forward), min(max_forward - r_proportional_control, max_forward)
    # time.sleep(0.01)


def follow_left(state_machine, rob, wall_dist=7.64):
    #rob = Robot()
##    print("following left")
    max_forward = rob.encoder.get_max_forward_speed()
    max_backward = rob.encoder.get_max_backward_speed()

    desired_distance = wall_dist
    # Proportional gain
    Kp = .2

    #user_input = input("Place robot beside wall and press enter to continue.")


    l_distance = rob.distance_sensor.get_left_inches()
    #f_distance = rob.distance_sensor.get_front_inches()

    l_proportional_control = saturation_function(Kp * (desired_distance - l_distance),
                                                    max_forward, max_backward)
    #f_proportional_control = saturation_function(Kp * (desired_distance - min(f_distance, l_distance)),
##                                                    max_forward, max_backward)

##    if f_distance < (desired_distance * 2):
##        rob.encoder.setSpeedsIPS(max_forward, min(max_forward + l_proportional_control, f_proportional_control,
##                                    max_forward))
    if l_distance < 0:
        pass
    else:
##        print("WF\n l_distance:{0}, l_speed:{1}\nr_distance:{2} r_speed:{3}".format(l_distance,
##                                                                                    min(max_forward - l_proportional_control, max_forward),
##                                                                                    rob.distance_sensor.get_right_inches(),
##                                                                                    min(max_forward + l_proportional_control, max_forward)))
        # rob.encoder.setSpeedsIPS(min(max_forward - l_proportional_control, max_forward),
        #                         min(max_forward + l_proportional_control, max_forward))
        return min(max_forward - l_proportional_control, max_forward), min(max_forward + l_proportional_control, max_forward)
    # time.sleep(0.01)

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

def follow_both(rob=None, next_cell = None, stopping_function=None):
    if rob is None or stopping_function is None:
        print("Error:Robot object was not passed")
        exit()
    while(stopping_function()):
        # print("moving to cell")
        lwall_dist = rob.distance_sensor.get_left_inches()
        rwall_dist = rob.distance_sensor.get_right_inches()

        if (lwall_dist < rob.cell_size) and (rwall_dist < rob.cell_size):
            lwall_lspeed, lwall_rspeed = follow_left(False, rob, (lwall_dist + rwall_dist) / 2)
            rwall_lspeed, rwall_rspeed = follow_right(False, rob, (lwall_dist + rwall_dist) / 2)
            rob.encoder.setSpeedsIPS((lwall_lspeed + rwall_lspeed) / 2, (lwall_rspeed + rwall_rspeed) / 2)
        elif lwall_dist < rob.cell_size:
            lwall_lspeed, lwall_rspeed = follow_left(False, rob)
            rob.encoder.setSpeedsIPS(lwall_lspeed, lwall_rspeed)
        elif rwall_dist < rob.cell_size:
            rwall_lspeed, rwall_rspeed = follow_right(False, rob)
            rob.encoder.setSpeedsIPS(rwall_lspeed, rwall_rspeed)
        else:
            rob.encoder.setSpeedsIPS(rob.encoder.get_max_forward_speed(), rob.encoder.get_max_forward_speed())
        # if rob.distance_sensor.get_right_inches() < rob.distance_sensor.get_left_inches():
        #     follow_right(False,rob)
        # else:
        #     follow_left(False,rob)
        time.sleep(0.01)

def main():
    from robot_class import Robot
    rob = Robot()
    while(True):
        if rob.distance_sensor.get_right_inches() < rob.distance_sensor.get_left_inches():
            follow_right(False,rob)
        else:
            follow_left(False,rob)
        

## Main program
if __name__ == "__main__":
    main()
