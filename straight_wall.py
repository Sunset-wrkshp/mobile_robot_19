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

rob = Robot()

desired_distance = 5
# Proportional gain
Kp = 1.5

user_input = input("Place robot in front of wall and press enter to continue.")

while (True):
    #r_distance = min(rob.distance_sensor.get_right_inches(), rob.distance_sensor.get_front_inches())
    r_distance = rob.distance_sensor.get_right_inches()
    f_distance = rob.distance_sensor.get_front_inches()
    if r_distance > 20:
        rob.encoder.stop()
    else:
        r_proportional_control = saturation_function(Kp * (desired_distance - r_distance),
                                                    rob.encoder.get_max_forward_speed(),
                                                    rob.encoder.get_max_backward_speed())
        f_proportional_control = saturation_function(Kp * ((desired_distance * 2) - f_distance),
                                                    rob.encoder.get_max_forward_speed(),
                                                    rob.encoder.get_max_backward_speed())
        if f_proportional_control == 0:
            f_proportional_control = 2 * rob.encoder.get_max_forward_speed()
        else:
            f_proportional_control = 1 / f_proportional_control
        
##        if f_distance < desired_distance:
##            rob.encoder.setSpeedsIPS(0,rob.encoder.get_max_forward_speed())
##        else:
        print("r distance: " + str(r_distance))
        print("f distance: " + str(f_distance))
        print("r sat:" + str(r_proportional_control))
        print("f sat:" + str(f_proportional_control))
        if r_distance > desired_distance:
            rob.encoder.setSpeedsIPS(rob.encoder.get_max_forward_speed() - abs(f_proportional_control), rob.encoder.get_max_forward_speed() - abs(r_proportional_control))
        else:
            rob.encoder.setSpeedsIPS(rob.encoder.get_max_forward_speed() - abs(r_proportional_control) - abs(f_proportional_control), rob.encoder.get_max_forward_speed())
    time.sleep(0.01)
