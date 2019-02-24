import json
import os

def get_calib():
    with open("calibration.txt", "r") as f:
        return json.load(f)

def set_calib(data):
    with open("calibration.txt", "w") as f:
        f.write(json.dumps(data, indent=4))
    #check if the file wrote correctly
    # if os.stat("calibration.txt").st_size != 0:
    #     return True
    # else:
    #     return False
    return True

if __name__ == '__main__':

    test = [(1,10), (2,9), (3,8), (4,7), (5,6), (6,5),(7,4), (8,3),(9,2),(10,1)]
    print(set_calib(test))
    print(get_calib())
