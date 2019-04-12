from wall_following import follow_right, follow_left
from robot_class import Robot
import random

#Class used for determining when a robot has moved to the next cell and when it is centered in it
class NextCell:
    def __init__(self, rob, initial_distance = 0, left_wall = False, right_wall = False):
        self.rob = rob
        self.initial_distance = initial_distance
        self.left_wall_detected = left_wall
        self.right_wall_detected = right_wall

    # used for moving to the next cell
    # returns false if robot should stop
    def move_to_cell(self):
        if self.rob.distance_sensor.get_front_inches() < (self.initial_distance - 9):
            return False
        if self.left_wall_detected:
            if (self.rob.distance_sensor.get_left_inches > self.rob.cell_size):
                return False
        else:
            if (self.rob.distance_sensor.get_left_inches < self.rob.cell_size):
                return False

        if self.right_wall_detected:
            if (self.rob.distance_sensor.get_right_inches > self.rob.cell_size):
                return False
        else:
             if (self.rob.distance_sensor.get_right_inches < self.rob.cell_size):
                 return False
        if self.rob.encoder.steps_to_move[0] == -1:
            return False
        return True

    # Used for centering robot in a cell
    # returns false if robot should stop
    def center_in_cell(self):
        if self.rob.distance_sensor.get_front_inches() < (self.initial_distance - 9):
            return False
        if self.rob.encoder.steps_to_move[0] == -1:
            return False
        return True


def Navigate(rob):
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
