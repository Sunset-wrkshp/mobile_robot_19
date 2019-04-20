from robot_class import Robot
import time
import statistics

rob = Robot()
while True:
    print("front " + str(rob.distance_sensor.get_front_inches()))
    print("left " + str(rob.distance_sensor.get_left_inches()))
    print("right " + str(rob.distance_sensor.get_right_inches()))
    print("Average side: " + str((rob.distance_sensor.get_right_inches() + rob.distance_sensor.get_left_inches()) / 2))
    # print(rob.distance_sensor.get_average(0.2))
    time.sleep(1)

# def trim(percent, arr):
#     num_to_trim = int(len(arr) * percent)
#     for i in range(num_to_trim):
#         del arr[0]
#         del arr[-1]
#
# rob = Robot()
# # rob.rotate('l')
# avg_dist = []
# for i in range(100):
#     # print("front" + str(rob.distance_sensor.get_front_inches()))
#     avg_dist.append((rob.distance_sensor.get_right_inches() + rob.distance_sensor.get_left_inches()) / 2)
#     time.sleep(0.1)
#
# trim(.1, avg_dist)
# print(statistics.mean(avg_dist))