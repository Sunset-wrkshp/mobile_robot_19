#State Machine (Moore)
from robot_class import Robot
from wall_following import follow_right as WF
from motionToGoal import motionToGoal as MTG
from faceGoal import faceGoal as GF
import time

class State():
    rob = None
    def __init__(self, robot_instance):
        print("Current State: {}".format(self))
        rob = robot_instance

    def event(self, event):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class start_state(State):

    def event(self, event=None):
##        return goal_facing(rob)
        #return wall_follow(rob)
        if rob.check_goal_in_front():
            if not rob.check_no_wall_in_front():
                return wall_follow(rob)
            else:
                return motion_to_goal(rob)
        else:
            return goal_facing(rob)
        #if goal in front but front wall detected: WF
        #if goal in front and no front wall detected: MTG
        #if goal is not in front: GF
        pass


class goal_facing(State):

    def event(self, event=None):
        GF(True, rob)
        if rob.goal_in_front():
            # print("I finished GF")
            return motion_to_goal(rob)
        elif (not rob.goal_in_front() and not rob.check_no_wall_in_front()):
            return wall_following(rob)
        else:
            return goal_facing(rob)

        #run goal facing
        #if goal is not in front and front sensor < 4 in: WF
        #If goal is in front: MTG
        #if goal not in front: GF

class motion_to_goal(State):

    def event(self, event=None):
        MTG(True, rob)
        if (rob.check_goal_in_front()):
            if (rob.stop_range()):
                return stop_state(rob)
            elif (not rob.check_no_wall_in_front()):
                return wall_follow(rob)
            else:
                return motion_to_goal(rob)
        else:
            if (not rob.check_no_wall_in_front()):
                return wall_follow(rob)
            else:
                return goal_facing(rob)
##        if goal_in_front():
##            return stop_state(rob)
##        else return motion_to_goal(rob)

        #run motion to goal
        #if goal is not in front and front wall detected <= 10cm: WF
        #if goal in front and 5 in of Goal: Stop
        #if goal is not in front and no wall detected: GF
        pass

class wall_follow(State):

    def event(self, event=None):
        WF(True, rob)
        if rob.goal_in_front():
            if rob.no_wall_detected():
                return motion_to_goal(rob)
            else:
                return goal_facing(rob)
        else:
            return wall_follow(rob)

        #run wall following
        #if goal is in front and front wall is not detected: MTG
        pass


class stop_state(State):
    
    def event(self, event=None):
        # return False
        #stop moving the robot
        rob.encoder.setSpeedsIPS(0,0)
##        t_set= []
##        for x in range (0,10):
##            t_set.append(rob.check_goal_in_front())
##        print(t_set)
            
        if (not rob.check_goal_in_front()):
            return goal_facing(rob)
        elif(rob.check_goal_in_front() and rob.check_no_wall_in_front()):
            f_distance = rob.distance_sensor.get_front_inches()
            if (f_distance > 5 and f_distance < 10):
                return motion_to_goal(rob)
            else:
                return stop_state(rob)
        else:
            return stop_state(rob)
        #if goal is not in front: GF
        #if goal is in front > 5 inch:  MTG
        #else: stop


class State_Machine():
    #Moore Machine
    state = None
    robot = None
    def __init__(self,rob):
        robot = rob
        self.state = start_state(rob)

    def run(self):
        while(self.state is not False):
            self.state = self.state.event()

def print_status():
    print("GIF:{0}, no_wall:{1}, <10cm:{2}, stop_r:{3}".format(rob.GIF, rob.no_wall, rob.less_than_10, rob.stop_r))


## testing code
if __name__ == '__main__':
    rob = Robot()

    SM = True

    SM = State_Machine(rob)
    SM.run()
##    GF(True, rob)
##    for s in range (0,100):
##        print(rob.check_no_wall_in_front())
##        print_status()
##    

    
    rob.stop()
# ##    for x in range(0,100):
# ##        rob.check_goal_in_front()
# ##        print_status()
#     print_status()
#     GF(True, rob)
#     print_status()
#     WF(True, rob)
#     print_status()
#     if (rob.check_goal_in_front()):
#         MTG(True, rob)
#         print_status()
#         if (rob.check_goal_in_front()):
#             rob.stop_range(True)
#     else:
#         print("oof")
#         print_status()
#     rob.stop()
#
#     # test = State_Machine()
#
#     # test.run()
