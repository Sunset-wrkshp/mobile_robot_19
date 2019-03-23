#State Machine (Moore)

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
        return goal_facing()
        #calibrate robot
        #if goal in front but front wall detected: WF
        #if goal in front and no front wall detected: MTG
        #if goal is not in front: GF
        pass


class goal_facing(State):

    def event(self, event=None):
        print("In goal facing right now")
        return motion_to_goal()
        #run goal facing
        #If goal is in sight and front wall <= 10cm: WF
        #If goal is sight and no wall >= 10 cm in front: MTG
        pass

class motion_to_goal(State):

    def event(self, event=None):
        return wall_follow()
        #run motion to goal
        #if front wall detected <= 10cm: WF
        #if <= 10 in of goal and no wall: PC

        pass

class wall_follow(State):

    def event(self, event=None):
        return proportion_control()
        #run wall following
        #if goal is in front and front wall is not detected: MTG
        pass

class proportion_control(State):

    #Moves the robot forward with proportion control when close to the goal without an obstacle
    def event(self, event=None):
        return stop_state()
        #Go forward with proportion control
        #If robot is within 5 inches (+- Error) of Goal: Stop
        #if robot is >= 10 inches from goal: MTG
        pass

class stop_state(State):

    def event(self, event=None):
        print("Finished")
        return False
        #stop moving the robot
        #if goal is not in front: GF
        #if goal is in front > 5 inch <= 10 inch: PC
        #if goal is in front > 10 inch: MTG
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
