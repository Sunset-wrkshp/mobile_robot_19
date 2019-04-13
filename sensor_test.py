from robot_class import Robot
import time

rob = Robot()
rob.rotate('l')
while True:
    print("front" + str(rob.distance_sensor.get_front_inches()))
    print("left" + str(rob.distance_sensor.get_left_inches()))
    print("right" + str(rob.distance_sensor.get_right_inches()))
    print()
    time.sleep(0.5)