from robot_class import Robot


while (true):
    for x in range(0,1):
        blobs = rob.camera.get_blobs(x)

        #Find largest blob
        largest = -1
        size = 0.0
        for i in range(len(blobs)):
            if blobs[i].size > size:
                size = blobs[i].size
                largest = i

        speed = 0
        if len(blobs) > 0:
            print("I found color {0}".format(x))
