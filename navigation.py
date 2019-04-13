#from wall_following import follow_right, follow_left
from robot_class import Robot
import random


def navigate(rob):
    while(True):
        available_directions = []
        if rob.distance_sensor.get_right_inches() > rob.cell_size:
            available_directions.append('r')
        if rob.distance_sensor.get_left_inches() > rob.cell_size:
            available_directions.append('l')
        if rob.distance_sensor.get_front_inches() > rob.cell_size:
            available_directions.append('f')

        if len(available_directions) > 0:
            direction = available_directions[random.randint(0, len(available_directions) - 1)]
        else:
            direction = 'b'

        if direction == 'r':
            rob.rotate('r')
        if direction == 'l':
            rob.rotate('l')
        if direction == 'b':
            rob.rotate('r')
            rob.rotate('r')

        rob.forward()

## Main program
if __name__ == "__main__":
    rob=Robot()
    #navigate(rob)
    rob.forward()