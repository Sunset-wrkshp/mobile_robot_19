from threading import Thread
from os import system, path
from robot_class import *
import time
from navigation import navigate

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
            # print("location = " + str(self.mapper.xy_to_cell(self.mapper.current_x, self.mapper.current_y) + 1)
                    # +"     orientation = " + self.mapper.rob.orientation.upper())
            self.user_input = input()


    def set_orientation(self):
        system('clear')
        user_input = input("Enter new orientation (n, s, e, w): ")
        if (user_input.lower() == 'n') or (user_input.lower() == 's') \
                or (user_input.lower() == 'e') or (user_input.lower() == 'w'):
            # self.mapper.rob.orientation = user_input
            pass
        else:
            print("Improper orientation")


    # def reset_map(self):
    #     user_input = input("Resetting map. Are you sure? (y/n): ")
    #     if user_input.lower() == 'y':
    #         self.mapper.walls = [[[], [], [], []],
    #                              [[], [], [], []],
    #                              [[], [], [], []],
    #                              [[], [], [], []]]
    #         self.mapper.mapped_cells = [[False, False, False, False],
    #                              [False, False, False, False],
    #                              [False, False, False, False],
    #                              [False, False, False, False]]

    def choose_color(self):
        system("clear")
        user_input = input("Enter Starting Color- (g)reen, (o)range, (p)ink, (b)lue: ")
        if (user_input.lower() == 'g') or (user_input.lower() == 'o') \
                or (user_input.lower() == 'p') or (user_input.lower() == 'b'):
            #process the starting color
            #get color location from the map
            #set robot starting location to that cell number/ (x,y)
            # user_input = int(user_input)
            # user_input -= 1
            # y = int(int(user_input) / 4)
            # x = int(user_input) % 4
            # self.mapper.current_x = x
            # self.mapper.current_y = y
            pass
        else:
            print("Improper Color.")
            return
        user_input = input("Enter Ending Color- (g)reen, (o)range, (p)ink, (b)lue: ")
        if (user_input.lower() == 'g') or (user_input.lower() == 'o') \
                or (user_input.lower() == 'p') or (user_input.lower() == 'b'):
            #process the ending color
            #get color location from the map
            #set robot ending location to that cell number/ (x,y)
            pass
        else:
            print("Improper color.")
            return

    def run(self):
        #check if a map exists
        # if (map_exists):
        #     run
        pass

def main():
    p = Path_Planning_Menu(1)


if __name__ == '__main__':
    main()
