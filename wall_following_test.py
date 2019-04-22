from robot_class import Robot
from wall_following import follow_left


rob = Robot()
Kp = 1
wall_dist = 7

while True:
    lwall_lspeed, lwall_rspeed = follow_left(False, rob, Kp, wall_dist)
    rob.encoder.setSpeedsIPS(lwall_lspeed, lwall_rspeed)