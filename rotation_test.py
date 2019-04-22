from robot_class import Robot
import time

rob = Robot()
while True:
    rob.center_rotate(rob.distance_sensor.get_left_inches)
    time.sleep(1)