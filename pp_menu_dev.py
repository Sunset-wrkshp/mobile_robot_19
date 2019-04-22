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
        if not all(self.mapper.mapped_cells):
            print("Empty Map. Load a Full Map first. ")
            return
        user_input = input("Enter Starting Color- (g)reen, (o)range, (p)ink, (b)lue: ")
        if (user_input.lower() == 'g') or (user_input.lower() == 'o') \
                or (user_input.lower() == 'p') or (user_input.lower() == 'b'):
            #process the starting color
            #get color location from the map
            self.mapper.rob.current_x = self.mapper.color_locations[user_input][0]
            self.mapper.rob.current_y = self.mapper.color_locations[user_input][1]
        else:
            print("Improper Color.")
            return
        user_input = input("Enter Ending Color- (g)reen, (o)range, (p)ink, (b)lue: ")
        if (user_input.lower() == 'g') or (user_input.lower() == 'o') \
                or (user_input.lower() == 'p') or (user_input.lower() == 'b'):
            #process the ending color
            #get color location from the map
            self.mapper.rob.end_x = self.mapper.color_locations[user_input][0]
            self.mapper.rob.end_y = self.mapper.color_locations[user_input][1]
        else:
            print("Improper color.")
            return

    def run(self):
        #check if a map exists
        if not all(self.mapper.mapped_cells):
            print("Empty Map. Load a Full Map first")
            return
        else:
            print(self.mapper.current_x)
            print(self.mapper.current_y)
            print(self.mapper.end_x)
            print(self.mapper.end_y)
            # self.mapper.follow_path(self.mapper.movement_planner())
            return

def main():
    p = Path_Planning_Menu(1)


if __name__ == '__main__':
    main()
