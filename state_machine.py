#State Machine (Moore)
import robot_class
from wall_following import follow_right as WF

class State():
    def __init__(self):
        print("Current State: {}".format(self))

    def event(self, event):
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class start_state(State):

    def event(self, event=None):
        #calibrate robot
        #if goal in front but front wall detected: WF
        #if goal in front and no front wall detected: MTG
        #if goal is not in front: GF
        pass


class goal_facing(State):

    def event(self, event=None):
        return motion_to_goal()
        #run goal facing
        #if goal is not in front and front sensor < 4 in: WF
        #If goal is in front: MTG
        #if goal not in front: GF

        pass

class motion_to_goal(State):

    def event(self, event=None):
        return wall_follow()
        #run motion to goal
        #if goal is not in front and front wall detected <= 10cm: WF
        #if goal in front and 5 in of Goal: Stop
        #if goal is not in front and no wall detected: GF
        pass

class wall_follow(State):

    def event(self, event=None):
        return proportion_control()
        #run wall following
        #if goal is in front and front wall is not detected: MTG
        pass


class stop_state(State):

    def event(self, event=None):
        print("Finished")
        return False
        #stop moving the robot
        #if goal is not in front: GF
        #if goal is in front > 5 inch:  MTG
        #else: stop
        pass


class State_Machine():
    #Moore Machine
    state = None
    def __init__(self):
        self.state = start_state()

    def run(self):
        while(self.state is not False):
            self.state = self.state.event()


## testing code
if __name__ == '__main__':
    test = State_Machine()

    test.run()
