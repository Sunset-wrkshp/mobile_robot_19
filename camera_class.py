# This program demonstrates advanced usage of the OpenCV library by
# using the SimpleBlobDetector feature along with camera threading.
# The program displays two windows: one for adjusting the mask,
# and one that displays the detected blobs in the (masked) image.
# Adjust the HSV values until blobs are detected from the camera feed.
# There's also a params file in the same folder that can be adjusted.

# Helpful links:
# https://www.learnopencv.com/blob-detection-using-opencv-python-c/
# https://docs.opencv.org/3.4.1/da/d97/tutorial_threshold_inRange.html
# https://docs.opencv.org/3.4.1/d0/d7a/classcv_1_1SimpleBlobDetector.html
# https://docs.opencv.org/3.4.1/d2/d29/classcv_1_1KeyPoint.html
# https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

import cv2 as cv
import time
from ThreadedWebcam import ThreadedWebcam
from UnthreadedWebcam import UnthreadedWebcam
from os import system

class Camera():

    FPS_SMOOTHING = 0.9
    SHOW_BLOBS = False

    # Window names
    WINDOW = "Adjustable Mask - Press Esc to quit"

    # Default HSV ranges
    # Note: the range for hue is 0-180, not 0-255


    # green
    color_0 = {'minH': 36, 'minS': 60, 'minV': 125,
               'maxH': 41, 'maxS': 255, 'maxV': 255}
    # orange
    color_1 = {'minH': 11, 'minS': 188, 'minV': 94,
               'maxH': 22, 'maxS': 255, 'maxV': 255}
    #pink
    color_2 = {'minH': 162, 'minS': 103, 'minV': 165,
               'maxH': 173, 'maxS': 237, 'maxV': 255}
    #blue
    color_3 = {'minH': 95, 'minS': 108, 'minV': 132,
               'maxH': 118, 'maxS': 210, 'maxV': 212}


    def __init__(self):
        # Initialize the threaded camera
        # You can run the unthreaded camera instead by changing the line below.
        # Look for any differences in frame rate and latency.
        self.camera = ThreadedWebcam() # UnthreadedWebcam()
        self.camera.start()

        # Initialize the SimpleBlobDetector
        params = cv.SimpleBlobDetector_Params()
        self.detector = cv.SimpleBlobDetector_create(params)

        # Attempt to open a SimpleBlobDetector parameters file if it exists,
        # Otherwise, one will be generated.
        # These values WILL need to be adjusted for accurate and fast blob detection.
        fs = cv.FileStorage("params.yaml", cv.FILE_STORAGE_READ); #yaml, xml, or json
        if fs.isOpened():
            self.detector.read(fs.root())
        else:
            print("WARNING: params file not found! Creating default file.")

            fs2 = cv.FileStorage("params.yaml", cv.FILE_STORAGE_WRITE)
            self.detector.write(fs2)
            fs2.release()

        fs.release()
        
        #set white balance for color detection
        system('v4l2-ctl -c white_balance_auto_preset=0')
        system('v4l2-ctl -c red_balance=1450')
        system('v4l2-ctl -c blue_balance=2300')
        
        if self.SHOW_BLOBS:
            # Create windows
            cv.namedWindow(self.WINDOW)

    def get_blobs(self, id=0):
        color = {}

        if (id == 0):
            #green
            color = self.color_0
        elif (id == 1):
            #orange
            color = self.color_1
        elif (id == 2):
            #pink
            color = self.color_2
        elif (id ==3):
            #blue
            color = self.color_3


        # Get a frame
        frame = self.camera.read()

        # Blob detection works better in the HSV color space
        # (than the RGB color space) so the frame is converted to HSV.
        frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Create a mask using the given HSV range
        mask = cv.inRange(frame_hsv, (color['minH'], color['minS'], color['minV']), (color['maxH'], color['maxS'], color['maxV']))

        # Run the SimpleBlobDetector on the mask.
        # The results are stored in a vector of 'KeyPoint' objects,
        # which describe the location and size of the blobs.
        keypoints = self.detector.detect(mask)

        if self.SHOW_BLOBS:
          # Display the frame
          cv.imshow(self.WINDOW, mask)

        return keypoints

    # Just stops the robot
    def stop(self):
        self.camera.stop()


    def ctrlC(self):
        print("Stopping camera")
        self.stop()

    def color_get(self):
        # ["green","orange", "pink", "blue"]
        color_list= [None,None,None,None]
        for x in range(0,4):
            t_list = []
            t_c = 0
            f_c = 0
            for y in range(0,12):
                blobs = self.get_blobs(x)
                if len(blobs) > 0:
##                    t_list.append(True)
                    t_c = t_c + 1
                    # print("found {}".format(color[x]))
                else:
                    f_c = f_c + 1
##                    t_list.append(False)
            #do majority rule instead?
            if (t_c > f_c):
                color_list[x] = True
            else:
                color_list[x] = False
##            if any(t_list):
##                color_list[x] = True
##            else:
##                color_list[x] = False
        print(color_list)
        
##        def only1(l):
        true_found = False
        index = -1
        for v in color_list:
            if v:
                # a True was found!
                if true_found:
                    # found too many True's
                    return False 
                else:
                    # found the first True
                    index = color_list.index(v)
                    true_found = True
        # found zero or one True value
        if not any(color_list):
            return None
        else:
            return index
##        for val in color_list:
##            if val == True:
##                return color_list.index(val)
##        return None


if __name__ == "__main__":
    cam = Camera()
    while(True):
##        for x in range(0,4):
##            blobs = cam.get_blobs(x)
##            color = ["green","orange", "pink", "blue"]
##            if len(blobs) > 0:
##                print("found {}".format(color[x]))
        print("Color found: {}".format(cam.color_get()))
        time.sleep(0.2)


    cam.stop()
