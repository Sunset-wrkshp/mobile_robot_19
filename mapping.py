from threading import Thread
from os import system, path
from robot_class import *
import time
from navigation import navigate
import json

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
        self.color_locations = {'o':[None, None], 'g':[None,None], 'p':[None,None], 'b':[None,None]}

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
            if (cell_y > 0) and ("n" not in self.walls[cell_y][cell_x]) and ('s' not in self.walls[cell_y - 1][cell_x]):
                if distances[cell_y - 1][cell_x] == -1:
                    wave_queue.append([cell_x, cell_y - 1])
                    distances[cell_y - 1][cell_x] = distances[cell_y][cell_x] + 1

            # check right
            if (cell_x < 3) and ("e" not in self.walls[cell_y][cell_x]) and ('w' not in self.walls[cell_y][cell_x + 1]):
                if distances[cell_y][cell_x + 1] == -1:
                    wave_queue.append([cell_x + 1, cell_y])
                    distances[cell_y][cell_x + 1] = distances[cell_y][cell_x] + 1

            # check down
            if (cell_y < 3) and ("s" not in self.walls[cell_y][cell_x]) and ('n' not in self.walls[cell_y + 1][cell_x]):
                if distances[cell_y + 1][cell_x] == -1:
                    wave_queue.append([cell_x, cell_y + 1])
                    distances[cell_y + 1][cell_x] = distances[cell_y][cell_x] + 1

            # check left
            if (cell_x > 0) and ("w" not in self.walls[cell_y][cell_x]) and ('e' not in self.walls[cell_y][cell_x - 1]):
                if distances[cell_y][cell_x - 1] == -1:
                    wave_queue.append([cell_x - 1, cell_y])
                    distances[cell_y][cell_x - 1] = distances[cell_y][cell_x] + 1

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

        pos_y = (self.current_y * 3) + 1
        pos_x = (self.current_x * 5) + 2
        map[pos_y] = map[pos_y][0:pos_x] + "@" + map[pos_y][pos_x + 1:]

        for line in map:
            print(line)
        # [green, orange, pink, blue] camera color_get()
        if self.color_locations['g'][0] is not None:
            print("green: ", self.xy_to_cell(self.color_locations['g'][1], self.color_locations['g'][0]))
        if self.color_locations['o'][0] is not None:
            print("orange: ", self.xy_to_cell(self.color_locations['o'][1], self.color_locations['o'][0]))
        if self.color_locations['p'][0] is not None:
            print("pink: ", self.xy_to_cell(self.color_locations['p'][1], self.color_locations['p'][0]))
        if self.color_locations['b'][0] is not None:
            print("blue: ", self.xy_to_cell(self.color_locations['b'][1], self.color_locations['b'][0]))

    def sensor_test(self):
        while self.user_input == None:
            system('clear')
            print("front " + str(self.rob.distance_sensor.get_front_inches()))
            print("left " + str(self.rob.distance_sensor.get_left_inches()))
            print("right " + str(self.rob.distance_sensor.get_right_inches()))
            print("Average side: " + str(
                (rob.distance_sensor.get_right_inches() + rob.distance_sensor.get_left_inches()) / 2))
            # print(rob.distance_sensor.get_average(0.2))
            time.sleep(1)
        system('clear')

    def calibration(self):
        user_input = 'c'
        while user_input.lower() != 'q':
            print("********************")
            print("Calibration")
            print("********************")
            print("C - Recalibrate servos")
            print("Mf - Change maximum distance in front")
            print("Ms - change maximum distance on side")
            print("Wk - Change wall following Kp value")
            print("Rk - Change rotation Kp value")
            print("Fk - Change front wall adjustment Kp value")
            print("Dt - Change distance threshold")
            print("Dc - Change wall distance percentage change")
            print("Wd - Change target wall distance")
            print("St - Sensor test")
            print("R - Change rotation multiplier")
            print("M - Change movement multiplier")
            print("T - Test rotation")
            print("F - Test forward movement")
            print("Q - Quit and return to main menu")
            user_input = input()
            system('clear')

            if user_input.lower() == 'wk':
                print("Current wall following Kp value: " + str(self.rob.wall_following_Kp))
                new_kp = input("Enter new Kp: ")
                self.rob.wall_following_Kp = float(new_kp)
                system('clear')
            elif user_input.lower() == 'mf':
                print("Current maximum front distance: " + str(self.rob.max_front_distance))
                new_dist = input("Enter new maximum front distance: ")
                self.rob.max_front_distance = float(new_dist)
                system('clear')
            elif user_input.lower() == 'ms':
                print("Current maximum side distance: " + str(self.rob.max_side_distance))
                new_dist = input("Enter new maximum side distance: ")
                self.rob.max_side_distance = float(new_dist)
                system('clear')
            elif user_input.lower() == 'st':
                self.user_input = None
                Thread(target=self.sensor_test).start()
                self.user_input = input()
                system('clear')
            elif user_input.lower() == 'wd':
                print("Current target wall distance: " + str(self.rob.dist_from_front_wall))
                new_dist = input("Enter new target wall distance: ")
                self.rob.dist_from_front_wall = float(new_dist)
                system('clear')
            elif user_input.lower() == 'dc':
                print("Current distance chagne percentage: " + str(self.rob.wall_distance_change))
                new_dist_change = input("Enter new distance change percentage: ")
                self.rob.wall_distance_change = float(new_dist_change)
                system('clear')
            elif user_input.lower() == 'rk':
                print("Current rotation Kp value: " + str(self.rob.rotation_Kp))
                new_rot_kp = input("Enter new rotation Kp: ")
                self.rob.rotation_Kp = float(new_rot_kp)
                system('clear')
            elif user_input.lower() == 'fk':
                print("Current front Kp value: " + str(self.rob.front_adjustment_Kp))
                new_front_kp = input("Enter new front Kp: ")
                self.rob.front_adjustment_Kp = float(new_front_kp)
                system('clear')
            elif user_input.lower() == 'dt':
                print("Current distance threshold: " + str(self.rob.dist_threshold))
                new_dist_thresh = input("Enter new distance threshold: ")
                self.rob.dist_threshold = float(new_dist_thresh)
                system('clear')
            elif user_input.lower() == 'r':
                print("Current rotation multiplier: " + str(self.rob.rotation_mult))
                new_rot_mult = input("Enter new rotation multiplier: ")
                self.rob.rotation_mult = float(new_rot_mult)
                system('clear')
            elif user_input.lower() == 'm':
                print("Current forward movement multiplier: " + str(self.rob.forward_mult))
                new_forward_mult = input("Enter new movement multiplier: ")
                self.rob.forward_mult = float(new_forward_mult)
                system('clear')
            elif user_input.lower() == 't':
                test_key = 'c'
                while test_key.lower() != 'q':
                    test_key = input("Press any key to rotate or enter 'q' to return")
                    if test_key.lower() != 'q':
                       self.rob.rotate()
                    system('clear')
            elif user_input.lower() == 'f':
                test_key = 'c'
                while test_key.lower() != 'q':
                    test_key = input("Press any key move forward or enter 'q' to return")
                    if test_key.lower() != 'q':
                        self.rob.forward()
                    #system('clear')
            elif user_input.lower() == 'c':
                self.rob.encoder.TESTING = False
                self.rob.encoder.calibrateSpeeds()
                system('clear')

        return

    def localization(self):
        localization = Localization_Menu(self)

    def mapping(self):
        mapping = Mapping_Menu(self)

    def path_planning(self):
        pp = Path_Planning_Menu(self)

    def follow_path(self, path):
        for direction in path:
            self.rob.change_orientation(direction)
            stopped_early = self.rob.forward()
            if stopped_early:
                return

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
            print("Q - quit")
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
        self.wall_samples = 10
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
            print("P - Print current map")
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
            elif user_input.lower() == 'p':
                self.mapper.draw_map()


    def save_map(self):
        print("Existing files are overwritten without warning")
        user_input = input("Save file as: ")
        user_input = user_input + ".txt"
        file = open(user_input, "w")

        file.write("walls\n")
        file.write(json.dumps(self.mapper.walls))

        file.write("\nmapped cells\n")
        file.write(json.dumps(self.mapper.mapped_cells))
        # for i in self.mapper.mapped_cells:
        #     for j in i:
        #         if j:
        #             file.write("T")
        #         else:
        #             file.write("F")
        #         file.write('\n')

        file.close()
        system('clear')
        return

    def load_map(self):
        user_input = input("Enter the file to load: ")
        user_input += ".txt"
        exists = path.isfile(user_input)
        if exists:
            file = open(user_input, "r")
            #skip first line
            data = file.readline()
##            print(data)
            #clear the current data
            self.mapper.walls = [[[], [], [], []],
                          [[], [], [], []],
                          [[], [], [], []],
                          [[], [], [], []]]
            self.mapper.mapped_cells = [[False, False, False, False],
                                 [False, False, False, False],
                                 [False, False, False, False],
                                 [False, False, False, False]]
            data = file.readline()
##            print(data)
            self.mapper.walls = json.loads(data)
            file.readline()
            self.mapper.mapped_cells = json.loads(file.readline())
        # if exists:
        #     file = open(user_input, "r")
        #     #skip first line
        #     data = file.readline()
        #     #clear the current data
        #     self.mapper.walls = [[[], [], [], []],
        #                   [[], [], [], []],
        #                   [[], [], [], []],
        #                   [[], [], [], []]]
        #     self.mapper.mapped_cells = [[False, False, False, False],
        #                          [False, False, False, False],
        #                          [False, False, False, False],
        #                          [False, False, False, False]]
        #
        #     for i in range(4):
        #         for j in range(4):
        #             data = file.readline()
        #             for char in data:
        #                 if (char == 'n') or (char == 'w') or (char == 's') or (char == 'e'):
        #                     self.mapper.walls[i][j].append(char)
        #             print()
        #     data = file.readline()
        #     data = file.readline()
        #     for i in range(4):
        #         for j in range(4):
        #             data = file.readline()
        #             if data == "T":
        #                 self.mapper.mapped_cells[i][j] = True
        #             elif data == "F":
        #                 self.mapper.mapped_cells[i][j] = False

            file.close()
            print(self.mapper.walls)
            print(self.mapper.mapped_cells)
            user_input = input("Press Enter to continue:")
            system('clear')
        else:
            print("File not found")
        return

    def map(self):
        # add front, left, and right walls
        self.add_walls()
        self.mapper.rob.rotate('r')
        # add back wall
        time.sleep(0.05)
        self.add_walls()
        time.sleep(0.05)

        while self.user_input == None:
            system('clear')
            self.mapper.draw_map()
            search_x = 0
            search_y = 0
            while (search_y < 4) and (self.mapper.mapped_cells[search_y][search_x]):
                while (search_x < 4) and (self.mapper.mapped_cells[search_y][search_x]):
                    search_x += 1
                if (search_x < 4) and (search_y < 4) and (self.mapper.mapped_cells[search_y][search_x] == False):
                    break
                else:
                    search_y += 1
                    search_x = 0
            if (search_y >= 4) or (search_x >= 4):
                system('clear')
                self.mapper.draw_map()
                print("All cells mapped. Press any key to continue.")
                return
            self.mapper.end_x = search_x
            self.mapper.end_y = search_y
            path = self.mapper.movement_planner()

            for direction in path:
                if self.user_input != None:
                    system('clear')
                    self.mapper.draw_map()
                    print("Press any key to continue.")
                    return

                self.mapper.mapped_cells[self.mapper.current_y][self.mapper.current_x] = True
                self.add_walls()
                system('clear')
                self.mapper.draw_map()
                self.mapper.rob.change_orientation(direction)

                # A wall is blocking the path
                if self.mapper.rob.distance_sensor.get_front_inches() < self.mapper.rob.max_front_distance:
                    self.mapper.rob.adjust_front_distance()
                    system('clear')
                    self.mapper.draw_map()
                    break
                # No wall, continue
                else:
                    stopped_early = self.mapper.rob.forward()
                    if stopped_early:
                        break
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

            self.mapper.mapped_cells[self.mapper.current_y][self.mapper.current_x] = True
            self.add_walls()
            system('clear')
            self.mapper.draw_map()

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
            self.adjust_map('x', 3 - cell_x)
        elif num_walls_w == 4:
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
            self.adjust_map('y', 3 - cell_y)
        elif num_walls_n == 4:
            self.adjust_map('y', 0 - cell_y)

        # check for gaps vetically
        if cell_x == 0:
            for y in range(4):
                if (self.mapper.mapped_cells[y][cell_x] == True) and ('w' not in self.mapper.walls[y][cell_x]):
                    self.adjust_map('x', 1)
                    cell_x += 1
                    break

        elif cell_x == 3:
            for y in range(4):
                if (self.mapper.mapped_cells[y][cell_x] == True) and ('e' not in self.mapper.walls[y][cell_x]):
                    self.adjust_map('x', -1)
                    cell_x -= 1
                    break

        # check for gaps horizontally
        if cell_y == 0:
            for x in range(4):
                if (self.mapper.mapped_cells[cell_y][x] == True) and ('n' not in self.mapper.walls[cell_y][x]):
                    self.adjust_map('y', 1)
                    cell_y += 1
                    break

        elif cell_y == 3:
            for x in range(4):
                if (self.mapper.mapped_cells[cell_y][x] == True) and ('s' not in self.mapper.walls[cell_y][x]):
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
            if self.mapper.color_locations['o'][1] is not None:
                self.mapper.color_locations['o'][1] += magnitude
            if self.mapper.color_locations['b'][1] is not None:
                self.mapper.color_locations['b'][1] += magnitude
            if self.mapper.color_locations['g'][1] is not None:
                self.mapper.color_locations['g'][1] += magnitude
            if self.mapper.color_locations['p'][1] is not None:
                self.mapper.color_locations['p'][1] += magnitude
        elif axis == 'y':
            for x in range(4):
                for y in range(max(0, 0 - magnitude), min(4, 4 - magnitude)):
                    new_walls[y + magnitude][x] = self.mapper.walls[y][x]
                    new_mapped[y + magnitude][x] = self.mapper.mapped_cells[y][x]
            self.mapper.current_y += magnitude
            if self.mapper.color_locations['o'][0] is not None:
                self.mapper.color_locations['o'][0] += magnitude
            if self.mapper.color_locations['b'][0] is not None:
                self.mapper.color_locations['b'][0] += magnitude
            if self.mapper.color_locations['g'][0] is not None:
                self.mapper.color_locations['g'][0] += magnitude
            if self.mapper.color_locations['p'][0] is not None:
                self.mapper.color_locations['p'][0] += magnitude

        self.mapper.mapped_cells = new_mapped
        self.mapper.walls = new_walls

    def add_walls(self):
        front_dir = self.mapper.rob.orientation
        left_dir = self.mapper.rob.get_left_dir()
        right_dir = self.mapper.rob.get_right_dir()
        needs_right_map = False
        needs_left_map = False
        new_walls = []

        num_f = 0
        num_t = 0
        #if front_dir not in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]:
        for i in range(self.wall_samples):
            if self.mapper.rob.distance_sensor.get_front_inches() < self.mapper.rob.max_front_distance:
                num_t += 1
            else:
                num_f += 1
            #time.sleep(0.01)
        if num_t > num_f:
            new_walls.append(front_dir)
            #self.mapper.walls[self.mapper.current_y][self.mapper.current_x].append(front_dir)
            time.sleep(0.1)
            self.mapper.rob.adjust_and_check_colors(mapper)
            time.sleep(0.1)

        num_f = 0
        num_t = 0
        #if left_dir not in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]:
        for i in range(self.wall_samples):
            if self.mapper.rob.distance_sensor.get_left_inches() < self.mapper.rob.cell_size:
                num_t += 1
            else:
                num_f += 1
            #time.sleep(0.01)
        if num_t > num_f:
            needs_left_map = True
            new_walls.append(front_dir)
            #self.mapper.walls[self.mapper.current_y][self.mapper.current_x].append(left_dir)

        num_f = 0
        num_t = 0
        #if right_dir not in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]:
        for i in range(self.wall_samples):
            if self.mapper.rob.distance_sensor.get_right_inches() < self.mapper.rob.cell_size:
                num_t += 1
            else:
                num_f += 1
            #time.sleep(0.01)
        if num_t > num_f:
            needs_right_map = True
            new_walls.append(front_dir)
            #self.mapper.walls[self.mapper.current_y][self.mapper.current_x].append(right_dir)

        self.mapper.walls[self.mapper.current_y][self.mapper.current_x] = new_walls

        if left_dir in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]:
            if needs_left_map:
                time.sleep(0.1)
                self.mapper.rob.change_orientation(left_dir)
                self.mapper.rob.adjust_and_check_colors(mapper)
                time.sleep(0.1)
            else:
                if (self.mapper.rob.distance_sensor.get_left_inches() < self.mapper.rob.max_side_distance) \
                        and abs(self.mapper.rob.distance_sensor.get_left_inches() - self.mapper.rob.dist_from_front_wall) > self.mapper.rob.dist_threshold:
                    time.sleep(0.1)
                    self.mapper.rob.change_orientation(left_dir)
                    self.mapper.rob.adjust_front_distance()
                    time.sleep(0.1)

        if right_dir in self.mapper.walls[self.mapper.current_y][self.mapper.current_x]:
            if needs_right_map:
                time.sleep(0.1)
                self.mapper.rob.change_orientation(right_dir)
                self.mapper.rob.adjust_and_check_colors(mapper)
                time.sleep(0.1)
            else:
                if (self.mapper.rob.distance_sensor.get_right_inches() < self.mapper.rob.max_side_distance) \
                        and abs(self.mapper.rob.distance_sensor.get_right_inches() - self.mapper.rob.dist_from_front_wall) > self.mapper.rob.dist_threshold:
                    time.sleep(0.1)
                    self.mapper.rob.change_orientation(right_dir)
                    self.mapper.rob.adjust_front_distance()
                    time.sleep(0.1)

        self.find_conflicts(self.mapper.current_x, self.mapper.current_y)

class Localization_Menu:
    def __init__(self, mapper):
        self.mapper = mapper
        self.user_input = None
        self.user_input = ''
        self.print_menu()
        # Thread(target = self.print_menu).start()
        # self.user_input = 'c'
        # while self.user_input.lower() != 'q':
        #     self.user_input = input()
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
            self.user_input = input()

            # for y in self.mapper.mapped_cells:
            #     for x in y:
            #         if x:
            #             print('x', end='')
            #         else:
            #             print('.', end='')
            #     print()
            #
            # print("********************")
            # time.sleep(1)

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
        if (user_input.isdigit()) and (int(user_input) > 0) and (int(user_input) <= 16):
            user_input = int(user_input)
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


class Path_Planning_Menu:
    def __init__(self, mapper):
        self.mapper = mapper
        self.user_input = None
        self.user_input = ''
        self.print_menu()
        system('clear')

    def print_menu(self):
        while self.user_input.lower() != 'q':
            system('clear')

            if self.user_input.lower() == 'd':
                self.set_orientation()
            elif self.user_input.lower() == 'c':
                self.choose_color()
            elif self.user_input.lower() == 'r':
                self.run()

            print("********************")
            print("Path Planning")
            print("********************")
            print("D - Specify robot's current orientation")
            print("C - Choose Start and End Colors")
            print("R - Run the Algorithm")
            print("Q - Quit and return to main menu")
            print("********************")
            print("location = " + str(self.mapper.xy_to_cell(self.mapper.current_x, self.mapper.current_y) + 1)
                    +"     orientation = " + self.mapper.rob.orientation.upper())
            self.user_input = input()


    def set_orientation(self):
        system('clear')
        user_input = input("Enter new orientation (n, s, e, w): ")
        if (user_input.lower() == 'n') or (user_input.lower() == 's') \
                or (user_input.lower() == 'e') or (user_input.lower() == 'w'):
            self.mapper.rob.orientation = user_input
            pass
        else:
            print("Improper orientation")

    def choose_color(self):
        system("clear")
        if not self.finished_map():
            print("Empty Map. Load a Full Map first. ")
            return
        user_input = input("Enter Starting Color- (g)reen, (o)range, (p)ink, (b)lue: ")
        if (user_input.lower() == 'g') or (user_input.lower() == 'o') \
                or (user_input.lower() == 'p') or (user_input.lower() == 'b'):
            #process the starting color
            #get color location from the map
            pos = self.mapper.color_locations[user_input]
            # print(pos)
            self.mapper.current_x = pos[0]
            self.mapper.current_y = pos[1]
        else:
            print("Improper Color.")
            return
        user_input = input("Enter Ending Color- (g)reen, (o)range, (p)ink, (b)lue: ")
        if (user_input.lower() == 'g') or (user_input.lower() == 'o') \
                or (user_input.lower() == 'p') or (user_input.lower() == 'b'):
            #process the ending color
            #get color location from the map
            pos = self.mapper.color_locations[user_input]
            # print(pos)
            self.mapper.end_x = pos[0]
            self.mapper.end_y = pos[1]
        else:
            print("Improper color.")
            return

    def run(self):
        #check if a map exists
        if not self.finished_map():
            print("Empty Map. Load a Full Map first")
            return
        else:
            # print(self.mapper.current_x)
            # print(self.mapper.current_y)
            # print(self.mapper.end_x)
            # print(self.mapper.end_y)
            self.mapper.follow_path(self.mapper.movement_planner())
            return

    def finished_map(self):
        for x in self.mapper.mapped_cells:
            if not all(x):
                return False
        return True

if __name__ == "__main__":
    rob = Robot()
    mapper = Mapper(rob)
    mapper.main_menu()
