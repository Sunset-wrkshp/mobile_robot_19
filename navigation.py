#from wall_following import follow_right, follow_left
from robot_class import Robot
import random


def navigate(rob):
    while True:
        available_directions = []
        if rob.distance_sensor.get_right_inches() > rob.cell_size:
            # print("right inches: " + str(rob.distance_sensor.get_right_inches()))
            available_directions.append('r')
        if rob.distance_sensor.get_left_inches() > rob.cell_size:
            # print("left inches: " + str(rob.distance_sensor.get_left_inches()))
            available_directions.append('l')
        if rob.distance_sensor.get_front_inches() > rob.max_front_distance:
            # print("front inches: " + str(rob.distance_sensor.get_front_inches()))
            available_directions.append('f')

        if len(available_directions) > 0:
            direction = available_directions[random.randint(0, len(available_directions) - 1)]
        else:
            # print("back:")
            # print("front inches: " + str(rob.distance_sensor.get_front_inches()))
            # print("left inches: " + str(rob.distance_sensor.get_left_inches()))
            # print("right inches: " + str(rob.distance_sensor.get_right_inches()))
            direction = 'b'

        if direction == 'r':
            print("Turning right")
            rob.rotate('r')
        if direction == 'l':
            print("Turning left")
            rob.rotate('l')
        if direction == 'b':
            print("U-turn")
            rob.rotate('r')
            rob.rotate('r')

        print("Moving forward")
        rob.forward()

## Main program
if __name__ == "__main__":
    rob=Robot()
    navigate(rob)
    #rob.rotate('r')