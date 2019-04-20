#from robot_class import Robot
import time as time

def follow_right(state_machine, rob, Kp = 0.5, wall_dist=7.64):
    max_forward = rob.encoder.get_max_forward_speed()# / 1.5
    max_backward = rob.encoder.get_max_backward_speed()# / 1.5

    desired_distance = wall_dist

    r_distance = rob.distance_sensor.get_right_inches()
    # print("follow right r_dist: ", r_distance)

    r_proportional_control = saturation_function(Kp * (desired_distance - r_distance),
                                                    max_forward, max_backward)
    # print("follow right l_prop_control: ", r_proportional_control)
    # print("follow right max_forward: ", max_forward)
    # print("follow right max_backward: ", max_backward)

    return min(max_forward + r_proportional_control, max_forward), min(max_forward - r_proportional_control, max_forward)


def follow_left(state_machine, rob, Kp = 0.5, wall_dist=7.64):
    max_forward = rob.encoder.get_max_forward_speed()# / 1.5
    max_backward = rob.encoder.get_max_backward_speed()# / 1.5

    desired_distance = wall_dist

    l_distance = rob.distance_sensor.get_left_inches()
    # print("follow left l_dist: ", l_distance)

    l_proportional_control = saturation_function(Kp * (desired_distance - l_distance),
                                                    max_forward, max_backward)
    # print("follow left l_prop_control: ", l_proportional_control)
    # print("follow left max_forward: ", max_forward)
    # print("follow left max_backward: ", max_backward)

    return min(max_forward - l_proportional_control, max_forward), min(max_forward + l_proportional_control, max_forward)

def saturation_function(proportional_speed, max_forward_speed, max_backward_speed):
    if proportional_speed > 0.1:
        if -proportional_speed < (max_backward_speed / 2):
            return max_backward_speed / 2
        # elif -proportional_speed > (max_backward_speed / 1.5):
        #     return max_backward_speed / 1.5
        else:
            return -proportional_speed
    elif proportional_speed < -0.1:
        if -proportional_speed > (max_forward_speed / 2):
            return max_forward_speed / 2
        # elif -proportional_speed < (max_forward_speed / 1.5):
        #     return max_forward_speed / 1.5
        else:
            return -proportional_speed
    else:
        return 0

def follow_both(rob, next_cell, stopping_function, Kp, wall_dist):
    if rob is None or stopping_function is None:
        print("Error:Robot object was not passed")
        exit()
    while(stopping_function()):
        #print("moving to cell")
        lwall_dist = rob.distance_sensor.get_left_inches()
        rwall_dist = rob.distance_sensor.get_right_inches()

        if (lwall_dist < rob.cell_size / 1.5) and (rwall_dist < rob.cell_size / 1.5) \
                and next_cell.right_wall_detected and next_cell.left_wall_detected:
#                and next_cell.should_follow_right and next_cell.should_follow_left:
            #print("following both")
            wall_dist = (lwall_dist + rwall_dist) / 2
            if (wall_dist < 8.25) and (wall_dist > 7.25):
                rob.dist_from_front_wall = wall_dist
            else:
                # print("wall dist change attempt: ", wall_dist)
                wall_dist = 7.75
            # print("**********")
            lwall_lspeed, lwall_rspeed = follow_left(False, rob, Kp, wall_dist) #, (lwall_dist + rwall_dist) / 2)
            rwall_lspeed, rwall_rspeed = follow_right(False, rob, Kp, wall_dist) #, (lwall_dist + rwall_dist) / 2)
            # print("follow both")
            # print("left: ", lwall_lspeed, lwall_rspeed)
            # print("right: ", rwall_lspeed, rwall_rspeed)
            # print("wall_dist: ", wall_dist)
            rob.encoder.setSpeedsIPS(max(lwall_lspeed, rwall_lspeed), max(lwall_rspeed, rwall_rspeed))

            # lwall_lspeed, lwall_rspeed = follow_left(False, rob, Kp, (lwall_dist + rwall_dist) / 2)
            # rwall_lspeed, rwall_rspeed = follow_right(False, rob, Kp, (lwall_dist + rwall_dist) / 2)
            #rob.encoder.setSpeedsIPS((lwall_lspeed + rwall_lspeed) / 2, (lwall_rspeed + rwall_rspeed) / 2)
        #elif (lwall_dist < rob.cell_size / 1.5) and next_cell.should_follow_left:
        elif (lwall_dist < rob.cell_size / 1.5) and next_cell.left_wall_detected:
            # print("following left")
            # if (rwall_dist >= rob.cell_size / 1):
            #     print("rwall_dist too large")
            # if next_cell.should_follow_right == False:
            #     print("next_cell says don't follow right")
            # print("**********")
            # print("left wall follow")
            # print("wall dist: ", wall_dist)
            lwall_lspeed, lwall_rspeed = follow_left(False, rob, Kp, wall_dist)
            # print("speeds: ", lwall_lspeed, lwall_rspeed)

            rob.encoder.setSpeedsIPS(lwall_lspeed, lwall_rspeed)
        elif (rwall_dist < rob.cell_size / 1.5) and next_cell.right_wall_detected:
        #elif (rwall_dist < rob.cell_size / 1.5) and next_cell.should_follow_right:
            # print("following right")
            # if (lwall_dist >= rob.cell_size / 1):
            #     print("lwall_dist too large")
            # if next_cell.should_follow_left == False:
            #     print("next_cell says don't follow left")
            rwall_lspeed, rwall_rspeed = follow_right(False, rob, Kp, wall_dist)
            rob.encoder.setSpeedsIPS(rwall_lspeed, rwall_rspeed)
        else:
            # print("following neither")
            # if (rwall_dist >= rob.cell_size / 1):
            #     print("rwall_dist too large")
            # if (lwall_dist >= rob.cell_size / 1):
            #     print("lwall_dist too large")
            # if next_cell.should_follow_left == False:
            #     print("next_cell says don't follow left")
            # if next_cell.should_follow_right == False:
            #     print("next_cell says don't follow right")
            rob.encoder.setSpeedsIPS(rob.encoder.get_max_forward_speed(), rob.encoder.get_max_forward_speed())
        # if rob.distance_sensor.get_right_inches() < rob.distance_sensor.get_left_inches():
        #     follow_right(False,rob)
        # else:
        #     follow_left(False,rob)
        time.sleep(0.01)
    rob.encoder.stop()

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
