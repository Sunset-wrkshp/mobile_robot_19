from robot_class import Robot

def saturation_function(proportional_speed, max_forward_speed, max_backward_speed):
    if proportional_speed > 0:
        if proportional_speed > 1:
            return max_forward_speed
        else
            return max_forward_speed * proportional_speed
    else:
        if proportional_speed < -1:
            return max_backward_speed
        else:
            return max_backward_speed * proportional_speed


def main():
    rob = Robot()

    desired_distance = 5
    # Proportional gain
    Kp = 0.9

    input("Place robot in front of wall and press enter to continue.")

    while (True):
        distance = rob.distance_sensor.get_front_inches()
        proportional_control = saturation_function(Kp * (desired_distance - distance), 
                                                    rob.encoder.get_max_forward_speed, 
                                                    rob.encoder.get_max_backward_speed)

        rob.encoder.setSpeedIPS(proportional_control, proportional_control)
        time.sleep(0.01)
