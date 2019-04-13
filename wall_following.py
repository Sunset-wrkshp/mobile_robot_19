from robot_class import Robot
import time as time

def follow_right(state_machine, rob):
    max_forward = rob.encoder.get_max_forward_speed()
    max_backward = rob.encoder.get_max_backward_speed()

    desired_distance = 5
    # Proportional gain
    Kp = 4

##    user_input = input("Place robot beside wall and press enter to continue.")

    while (True):
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

        if f_distance < (desired_distance * 2):
            #front wall is deteced withing distance*2 inches. Starts to turn
            print("Turning")
            rob.encoder.setSpeedsIPS(min(max_forward + r_proportional_control, f_proportional_control,
                                        max_forward), max_forward)
        else:
            if (state_machine and (r_distance > (desired_distance * 20))):
                print("going straight")
                rob.encoder.setSpeedsIPS(max_forward,
                                        max_forward)
            else:
                #No front wall detected
                print("WF\n l_distance:{0}, l_speed:{1}\nr_distance:{2} r_speed:{3}".format(r_distance,
                                                                                            min(max_forward - r_proportional_control, max_forward),
                                                                                            rob.distance_sensor.left_inches(),
                                                                                            min(max_forward + r_proportional_control, max_forward)))
                print("Wall following")
                rob.encoder.setSpeedsIPS(min(max_forward + r_proportional_control, max_forward),
                                        min(max_forward - r_proportional_control, max_forward))
        time.sleep(0.01)


def follow_left(state_machine, rob):
    #rob = Robot()
    max_forward = rob.encoder.get_max_forward_speed()
    max_backward = rob.encoder.get_max_backward_speed()

    desired_distance = 5
    # Proportional gain
    Kp = 4.7

    user_input = input("Place robot beside wall and press enter to continue.")

    while (True):
        l_distance = rob.distance_sensor.get_left_inches()
        f_distance = rob.distance_sensor.get_front_inches()

        l_proportional_control = saturation_function(Kp * (desired_distance - l_distance),
                                                        max_forward, max_backward)
        f_proportional_control = saturation_function(Kp * (desired_distance - min(f_distance, l_distance)),
                                                        max_forward, max_backward)

        if f_distance < (desired_distance * 2):
            rob.encoder.setSpeedsIPS(max_forward, min(max_forward + l_proportional_control, f_proportional_control,
                                        max_forward))
        else:
            print("WF\n l_distance:{0}, l_speed:{1}\nr_distance:{2} r_speed:{3}".format(l_distance,
                                                                                        min(max_forward - l_proportional_control, max_forward),
                                                                                        rob.distance_sensor.get_right_inches(),
                                                                                        min(max_forward + l_proportional_control, max_forward)))
            rob.encoder.setSpeedsIPS(min(max_forward - l_proportional_control, max_forward),
                                    min(max_forward + l_proportional_control, max_forward))
        time.sleep(0.01)

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

def main():
    rob = Robot()
    if rob.distance_sensor.get_right_inches() < rob.distance_sensor.get_left_inches():
        follow_left(False,rob)
    else:
        follow_left(False,rob)

## Main program
if __name__ == "__main__":
    main()
