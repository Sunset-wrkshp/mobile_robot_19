#from wall_following import follow_right, follow_left
from robot_class import Robot
import random

def navigate(rob):
    wall_samples = 10
    while True:
        available_directions = []

        num_t = 0
        num_f = 0
        for i in range(wall_samples):
            if rob.distance_sensor.get_right_inches() < (rob.cell_size / 1.5):
                num_t += 1
            else:
                num_f += 1
            # time.sleep(0.01)
        if num_f > num_t:
            available_directions.append('r')

        num_t = 0
        num_f = 0
        for i in range(wall_samples):
            if rob.distance_sensor.get_left_inches() < (rob.cell_size / 1.5):
                num_t += 1
            else:
                num_f += 1
            # time.sleep(0.01)
        if num_f > num_t:
            available_directions.append('l')

        num_t = 0
        num_f = 0
        for i in range(wall_samples):
            if rob.distance_sensor.get_front_inches() < (rob.cell_size / 1.5):
                num_t += 1
            else:
                num_f += 1
            # time.sleep(0.01)
        if num_f > num_t:
            available_directions.append('f')

        if len(available_directions) > 0:
            direction = available_directions[random.randint(0, len(available_directions) - 1)]
        else:
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