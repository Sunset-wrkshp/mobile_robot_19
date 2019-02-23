from robot_class import Robot
import time as time

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

    desired_distance = 5
    # Proportional gain
    Kp = 1.5

    user_input = input("Place robot in front of wall and press enter to continue.")
    #print("max forward speed: " + str(rob.encoder.get_max_forward_speed()))
    #print("max backward speed: " + str(rob.encoder.get_max_backward_speed()))

    while (True):
        distance = rob.distance_sensor.get_front_inches()
        #print("Distance: " + str(distance))
        proportional_control = saturation_function(Kp * (desired_distance - distance), 
                                                    rob.encoder.get_max_forward_speed(), 
                                                    rob.encoder.get_max_backward_speed())
        #print("Pre_sat:" + str(Kp * (desired_distance - distance)))
        #print("PC: " + str(proportional_control))
        rob.encoder.setSpeedsIPS(proportional_control, proportional_control)
        time.sleep(0.01)

## Main program
if __name__ == "__main__":
    main()