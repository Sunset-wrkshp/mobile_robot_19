from tkinter import *
import math
from threading import Thread
from os import system, path
import time
from robot_class import *


class Mapper:
    def __init__(self, rob, start_x = 0, start_y = 0, end_x = 0, end_y = 0):
        self.rob = rob
        self.current_x = start_x
        self.current_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.end_cell = self.xy_to_cell(self.end_x, self.end_y)
        self.walls = [[[], [], [], []],
                      [[], [], [], []],
                      [[], [], [], []],
                      [[], [], [], []]]
        self.mapped_cells = [[False, False, False, False],
                             [False, False, False, False],
                             [False, False, False, False],
                             [False, False, False, False]]
        self.color_locations = [[], [], [], []]

    def xy_to_cell(self, cell_x, cell_y):
        return (cell_y * 4) + cell_x

    #   Expects "walls" to be a 2D array storing which walls border the cells
    #   Walls should be indicated as "n," "s," "e," and "w."
    def wave_maker(self):
        distances = [[-1, -1, -1, -1],
                     [-1, -1, -1, -1],
                     [-1, -1, -1, -1],
                     [-1, -1, -1, -1]]
        distances[self.end_y][self.end_x] = 0
        wave_queue = [[self.end_x, self.end_y]]
        while len(wave_queue) > 0:
            cell_x = wave_queue[0][0]
            cell_y = wave_queue[0][1]
            cell_num = self.xy_to_cell(cell_x, cell_y)
            wave_queue.pop(0)

            # if (cell_x == self.current_x) and (cell_y == self.current_y):
            #     return distances

            # check up
            if (cell_y > 0) and ("n" not in self.walls[cell_y][cell_x]):
                if distances[cell_y - 1][cell_x] == -1:
                    wave_queue.append([cell_x, cell_y - 1])
                    distances[cell_y - 1][cell_x] = distances[cell_y][cell_x] + 1

            # check right
            if (cell_x < 3) and ("e" not in self.walls[cell_y][cell_x]):
                if distances[cell_y][cell_x + 1] == -1:
                    wave_queue.append([cell_x + 1, cell_y])
                    distances[cell_y][cell_x + 1] = distances[cell_y][cell_x] + 1

            # check down
            if (cell_y < 3) and ("s" not in self.walls[cell_y][cell_x]):
                if distances[cell_y + 1][cell_x] == -1:
                    wave_queue.append([cell_x, cell_y + 1])
                    distances[cell_y + 1][cell_x] = distances[cell_y][cell_x] + 1

            # check left
            if (cell_x > 0) and ("w" not in self.walls[cell_y][cell_x]):
                if distances[cell_y][cell_x - 1] == -1:
                    wave_queue.append([cell_x - 1, cell_y])
                    distances[cell_y][cell_x - 1] = distances[cell_y][cell_x] + 1

        print(distances)
        return distances

    def movement_planner(self):
        distances = self.wave_maker()

        cell_x = self.current_x
        cell_y = self.current_y
        path = []
        while (cell_x != self.end_x) or (cell_y != self.end_y):
            north = float("inf")
            south = float("inf")
            east = float("inf")
            west = float("inf")

            # check up
            if (cell_y > 0) and ("n" not in self.walls[cell_y][cell_x]) and (distances[cell_y - 1][cell_x] != -1):
                north = distances[cell_y - 1][cell_x]

            # check left
            if (cell_x < 3) and ("e" not in self.walls[cell_y][cell_x]) and (distances[cell_y][cell_x + 1] != -1):
                east = distances[cell_y][cell_x + 1]

            # check down
            if (cell_y < 3) and ("s" not in self.walls[cell_y][cell_x]) and (distances[cell_y + 1][cell_x] != -1):
                south = distances[cell_y + 1][cell_x]

            # check right
            if (cell_x > 0) and ("w" not in self.walls[cell_y][cell_x]) and (distances[cell_y][cell_x - 1] != -1):
                west = distances[cell_y][cell_x - 1]

            min_dist = min(north, south, east, west)

            if min_dist == north:
                path.append("n")
                cell_y -= 1
            elif min_dist == east:
                path.append("e")
                cell_x += 1
            elif min_dist == south:
                path.append("s")
                cell_y += 1
            elif min_dist == west:
                path.append("w")
                cell_x -= 1

        return path

    def draw_map(self):
        map = ["*    *    *    *    *",
               "                     ",
               "                     ",
               "*    *    *    *    *",
               "                     ",
               "                     ",
               "*    *    *    *    *",
               "                     ",
               "                     ",
               "*    *    *    *    *",
               "                     ",
               "                     ",
               "*    *    *    *    *",]

        for x in range(4):
            for y in range(4):
                if self.mapped_cells[y][x]:
                    if 'n' in self.walls[y][x]:
                        map[(y * 3)] = map[(y * 3)][0:(x * 5) + 1] + "____" + map[(y * 3)][(x * 5) + 5:]
                    if 's' in self.walls[y][x]:
                        map[(y * 3) + 3] = map[(y * 3) + 3][0:(x * 5) + 1] + "____" + map[(y * 3) + 3][(x * 5) + 5:]
                    if 'e' in self.walls[y][x]:
                        map[(y * 3) + 1] = map[(y * 3) + 1][0:(x * 5) + 5] + "|" + map[(y * 3) + 1][(x * 5) + 6:]
                        map[(y * 3) + 2] = map[(y * 3) + 2][0:(x * 5) + 5] + "|" + map[(y * 3) + 2][(x * 5) + 6:]
                    if 'w' in self.walls[y][x]:
                        map[(y * 3) + 1] = map[(y * 3) + 1][0:(x * 5)] + "|" + map[(y * 3) + 1][(x * 5) + 1:]
                        map[(y * 3) + 2] = map[(y * 3) + 2][0:(x * 5)] + "|" + map[(y * 3) + 2][(x * 5) + 1:]
                else:
                    map[(y * 3) + 1] = map[(y * 3) + 1][0:(x * 5) + 1] + "????" + map[(y * 3) + 1][(x * 5) + 5:]
                    map[(y * 3) + 2] = map[(y * 3) + 2][0:(x * 5) + 1] + "????" + map[(y * 3) + 2][(x * 5) + 5:]

        for line in map:
            print(line)

    def calibration(self):
        input = 'c'
        while input.lower() != 'q':
            print("********************")
            print("Calibration")
            print("********************")
            print("Q - Quit and return to main menu")
        return

    def localization(self):
        localization = Localization_Menu(self)

    def mapping(self):
        mapping = Mapping_Menu(self)

    def path_planning(self):
        return

    def follow_path(self, path):
        for direction in path:
            self.rob.change_orientation(direction)
            self.rob.forward()

    def main_menu(self):
        user_input = 'C'
        system('clear')
        while user_input.lower() != 'q':
            print("********************")
            print("Main Menu")
            print("********************")

            print("C - Calibration")
            print("L - Localization")
            print("M - Mapping")
            print("P - Path Planning")
            print("Q - quit\n")
            user_input = input()
            system('clear')

            if user_input.lower() == 'c':
                self.calibration()
            elif user_input.lower() == 'l':
                self.localization()
            elif user_input.lower() == 'm':
                self.mapping()
            elif user_input.lower() == 'p':
                self.path_planning()
        self.rob.stop()


class Mapping_Menu:
    def __init__(self, mapper, debug=False):
        self.mapper = mapper
        self.display_menu()

    def display_menu(self):
        user_input = ''
        while user_input.lower() != 'q':
            print("********************")
            print("Mapping")
            print("********************")
            print("M - Start mapping")
            print("L - Load map")
            print("S - Save map")
            print("Q - quit and return to main menu")
            user_input = input()
            system('clear')

            if user_input.lower() == 'm':
                self.user_input = None
                Thread(target=self.map).start()
                self.user_input = input()
            elif user_input.lower() == 'l':
                self.load_map()
            elif user_input.lower() == 's':
                self.save_map()

    def save_map(self):
        print("Existing files are overwritten without warning")
        user_input = input("Save file as: ")
        file = open(user_input, "w")

        file.write("walls")
        for i in self.mapper.walls:
            for j in i:
                file.write(j)

        file.write("\nmapped cells")
        for i in self.mapper.mapped_cells:
            for j in i:
                file.write(j)

        file.close()
        system('clear')
        return

    def load_map(self):
        user_input = input("Enter the file to load: ")
        exists = path.isfile(user_input)
        if exists:
            file = open(user_input, "r")

            file.close()
            system('clear')
        else:
            print("File not found")
        return

    def map(self):
        # add front, left, and right walls
        self.add_walls()
        self.mapper.rob.rotate('r')
        # add back wall
        time.sleep(0.1)
        self.add_walls()
        time.sleep(0.1)

        while self.user_input == None:
            # system('clear')
            self.mapper.draw_map()
            search_x = 0
            search_y = 0
            print("searching map")
            while (search_y < 4) and (self.mapper.mapped_cells[search_y][search_x]):
                while (search_x < 4) and (self.mapper.mapped_cells[search_y][search_x]):
                    search_x += 1
                if (search_x < 4) and (search_y < 4) and (self.mapper.mapped_cells[search_y][search_x] == False):
                    break
                else:
                    search_y += 1
                    search_x = 0
            if (search_y >= 4) or (search_x >= 4):
                # system('clear')
                self.mapper.draw_map()
                print("All cells mapped. Press any key to continue.")
                return
            self.mapper.end_x = search_x
            self.mapper.end_y = search_y
            print("Planning path")
            path = self.mapper.movement_planner()

            for direction in path:
                if self.user_input != None:
                    # system('clear')
                    self.mapper.draw_map()
                    print("Press any key to continue.")
                    return

                self.add_walls()
                self.mapper.mapped_cells[self.mapper.current_y][self.mapper.current_x] = True
                self.mapper.rob.change_orientation(direction)

                # A wall is blocking the path
                if self.mapper.rob.distance_sensor.get_front_inches() < self.mapper.rob.max_front_distance:
                    print("wall in front")
                    break
                # No wall, continue
                else:
                    self.mapper.rob.forward()
                    orientation = self.mapper.rob.orientation.lower()
                    if orientation == 'n':
                        self.mapper.current_y -= 1
                    elif orientation == 'e':
                        self.mapper.current_x += 1
                    elif orientation == 's':
                        self.mapper.current_y += 1
                    elif orientation == 'w':
                        self.mapper.current_x -= 1
                    else:
                        print("Improper value stored in rob.orientation. Should be 'n', 'e', 'w', or 's'")

            print("adding walls")
            self.add_walls()
            print("stopped in cell")
            self.mapper.mapped_cells[self.mapper.current_y][self.mapper.current_x] = True

        if self.user_input != None:
            system('clear')
            self.mapper.draw_map()
            print("Press any key to continue.")
            return

    # Searches the map to determine if it needs to be adjusted
    def find_conflicts(self, cell_x, cell_y):
        # Check for conflicts vertically
        num_walls_e = 0
        num_walls_w = 0
        for y in range(4):
            if ('e' in self.mapper.walls[y][cell_x]) and (cell_x < 3):
                num_walls_e += 1
            if ('w' in self.mapper.walls[y][cell_x]) and (cell_x > 0):
                num_walls_w += 1
        if num_walls_e == 4:
            #print("E conflicted detected on y axis")
            self.adjust_map('x', 3 - cell_x)
        elif num_walls_w == 4:
            #print("W conflicted detected on y axis")
            self.adjust_map('x', 0 - cell_x)

        # Check for conflicts horizontally
        num_walls_n = 0
        num_walls_s = 0
        for x in range(4):
            if ('n' in self.mapper.walls[cell_y][x]) and (cell_y > 0):
                num_walls_n += 1
            if ('s' in self.mapper.walls[cell_y][x]) and (cell_y < 3):
                num_walls_s += 1
        if num_walls_s == 4:
            #print("S conflicted detected on x axis")
            self.adjust_map('y', 3 - cell_y)
        elif num_walls_n == 4:
            #print("N conflicted detected on x axis")
            self.adjust_map('y', 0 - cell_y)

        # check for gaps vetically
        if cell_x == 0:
            for y in range(4):
                if (self.mapper.mapped_cells[y][cell_x] == True) and ('w' not in self.mapper.walls[y][cell_x]):
                    #print("Gap detected on x axis")
                    self.adjust_map('x', 1)
                    cell_x += 1
                    break

        elif cell_x == 3:
            for y in range(4):
                if (self.mapper.mapped_cells[y][cell_x] == True) and ('e' not in self.mapper.walls[y][cell_x]):
                    #print("Gap detected on x axis")
                    self.adjust_map('x', -1)
                    cell_x -= 1
                    break

        # check for gaps horizontally
        if cell_y == 0:
            for x in range(4):
                if (self.mapper.mapped_cells[cell_y][x] == True) and ('n' not in self.mapper.walls[cell_y][x]):
                    #print("Gap detected on y axis")
                    self.adjust_map('y', 1)
                    cell_y += 1
                    break

        elif cell_y == 3:
            for x in range(4):
                if (self.mapper.mapped_cells[cell_y][x] == True) and ('s' not in self.mapper.walls[cell_y][x]):
                    #print("Gap detected on y axis")
                    self.adjust_map('y', -1)
                    cell_y -= 1
                    break

    # Adjusts the entire map on the x or y axis for a given magnitude
    def adjust_map(self, axis, magnitude):
        new_walls = [[[], [], [], []],
                     [[], [], [], []],
                     [[], [], [], []],
                     [[], [], [], []]]
        new_mapped = [[False, False, False, False],
                      [False, False, False, False],
                      [False, False, False, False],
                      [False, False, False, False]]
        if axis == 'x':
            for y in range(4):
                for x in range(max(0, 0 - magnitude), min(4, 4 - magnitude)):
                    new_walls[y][x + magnitude] = self.mapper.walls[y][x]
                    new_mapped[y][x + magnitude] = self.mapper.mapped_cells[y][x]
            self.mapper.current_x += magnitude
        elif axis == 'y':
            for x in range(4):
                for y in range(max(0, 0 - magnitude), min(4, 4 - magnitude)):
                    new_walls[y + magnitude][x] = self.mapper.walls[y][x]
                    new_mapped[y + magnitude][x] = self.mapper.mapped_cells[y][x]
            self.mapper.current_y += magnitude

        self.mapper.mapped_cells = new_mapped
        self.mapper.walls = new_walls


    def add_walls(self):
        front_dir = self.mapper.rob.orientation
        left_dir = self.mapper.rob.get_left_dir()
        right_dir = self.mapper.rob.get_right_dir()

        if (self.mapper.rob.distance_sensor.get_front_inches() < self.mapper.rob.max_front_distance) and (
                front_dir not in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]):
            # print("front wall found")
            self.mapper.walls[self.mapper.current_y][self.mapper.current_x].append(front_dir)
        if (self.mapper.rob.distance_sensor.get_left_inches() < (self.mapper.rob.cell_size / 2)) and (
                left_dir not in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]):
            # print("left wall found")
            self.mapper.walls[self.mapper.current_y][self.mapper.current_x].append(left_dir)
            self.mapper.walls[self.mapper.current_y][self.mapper.current_x].append(left_dir)
        if (self.mapper.rob.distance_sensor.get_right_inches() < (self.mapper.rob.cell_size / 2)) and (
                right_dir not in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]):
            # print("right wall found")
            self.mapper.walls[self.mapper.current_y][self.mapper.current_x].append(right_dir)

        self.find_conflicts(self.mapper.current_x, self.mapper.current_y)
        # print("******")

class Localization_Menu:
    def __init__(self, mapper):
        self.mapper = mapper
        self.user_input = None
        Thread(target = self.print_menu).start()
        self.user_input = 'c'
        while self.user_input.lower() != 'q':
            self.user_input = input()
        system('clear')

    def print_menu(self):
        while self.user_input.lower() != 'q':
            system('clear')

            if self.user_input.lower() == 'd':
                self.set_orientation()
            elif self.user_input.lower() == 'c':
                self.set_cell_number()
            elif self.user_input.lower() == 'r':
                self.reset_map()

            print("********************")
            print("Localization")
            print("********************")
            print("D - Specify robot's current orientation")
            print("C - Specify the robot's current cell number")
            print("R - Reset map")
            print("Q - Quit and return to main menu")
            print("********************")
            print("location = " + str(self.mapper.xy_to_cell(self.mapper.current_x, self.mapper.current_y) + 1)
                    +"     orientation = " + self.mapper.rob.orientation.upper())

            for y in self.mapper.mapped_cells:
                for x in self.mapper.mapped_cells[y]:
                    if self.mapper.mapped_cells[y][x]:
                        print('x', end='')
                    else:
                        print('.', end='')
                print()

            print("********************")
            time.sleep(1)

    def set_orientation(self):
        system('clear')
        user_input = input("Enter new orientation (n, s, e, w): ")
        if (user_input.lower() == 'n') or (user_input.lower() == 's') \
                or (user_input.lower() == 'e') or (user_input.lower() == 'w'):
            self.mapper.rob.orientation = user_input
        else:
            print("Improper orientation")

    def set_cell_number(self):
        system('clear')
        user_input = input("Enter cell number (1-16): ")
        if (user_input.isdigit()) and (user_input > 0) and (user_input <= 16):
            user_input -= 1
            y = int(int(user_input) / 4)
            x = int(user_input) % 4
            self.mapper.current_x = x
            self.mapper.current_y = y
        else:
            print("Improper cell number: ")

    def reset_map(self):
        user_input = input("Resetting map. Are you sure? (y/n): ")
        if user_input.lower() == 'y':
            self.mapper.walls = [[[], [], [], []],
                                 [[], [], [], []],
                                 [[], [], [], []],
                                 [[], [], [], []]]
            self.mapper.mapped_cells = [[False, False, False, False],
                                 [False, False, False, False],
                                 [False, False, False, False],
                                 [False, False, False, False]]


if __name__ == "__main__":
    #t1 = threading.Thread(target=main_menu, args=())
    rob = Robot()
    mapper = Mapper(rob)
    mapper.main_menu()