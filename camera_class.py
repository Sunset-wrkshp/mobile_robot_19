# Camera Class
#combine the threaded class and blob file.
#Update function to set the next state
#

import cv2 as cv
import time
from ThreadedWebcam import ThreadedWebcam
from UnthreadedWebcam import UnthreadedWebcam

class Camera():
    FPS_SMOOTHING = 0.9

    # Window names
    WINDOW1 = "Adjustable Mask - Press Esc to quit"
    WINDOW2 = "Detected Blobs - Press Esc to quit"

    # Default HSV ranges
    # Note: the range for hue is 0-180, not 0-255
    minH =   0; minS = 127; minV =   0;
    maxH = 180; maxS = 255; maxV = 255;

    #camera object
    camera = None;

    def __init__(self):
        # Initialize the threaded camera
        # You can run the unthreaded camera instead by changing the line below.
        # Look for any differences in frame rate and latency.
        camera = ThreadedWebcam() # UnthreadedWebcam()
        camera.start()

        # Initialize the SimpleBlobDetector
        params = cv.SimpleBlobDetector_Params()
        detector = cv.SimpleBlobDetector_create(params)

        # Attempt to open a SimpleBlobDetector parameters file if it exists,
        # Otherwise, one will be generated.
        # These values WILL need to be adjusted for accurate and fast blob detection.
        fs = cv.FileStorage("params.yaml", cv.FILE_STORAGE_READ); #yaml, xml, or json
        if fs.isOpened():
            detector.read(fs.root())
        else:
            print("WARNING: params file not found! Creating default file.")

            fs2 = cv.FileStorage("params.yaml", cv.FILE_STORAGE_WRITE)
            detector.write(fs2)
            fs2.release()

        fs.release()


    def read(self):
        return camera.read()

    def stop(self):
        camera.stop()

    # These functions are called when the user moves a trackbar
    def onMinHTrackbar(self, val):
        # Calculate a valid minimum red value and re-set the trackbar.
        self.minH = min(val, self.maxH - 1)
        cv.setTrackbarPos("Min Hue", self.WINDOW1, self.minH)

    def onMinSTrackbar(self,val):
        self.minS = min(val, self.maxS - 1)
        cv.setTrackbarPos("Min Sat", self.WINDOW1, self.minS)

    def onMinVTrackbar(self,val):
        self.minV = min(val, self.maxV - 1)
        cv.setTrackbarPos("Min Val", self.WINDOW1, self.minV)

    def onMaxHTrackbar(self,val):
        self.maxH = max(val, self.minH + 1)
        cv.setTrackbarPos("Max Hue", self.WINDOW1, self.maxH)

    def onMaxSTrackbar(self,val):
        self.maxS = max(val, self.minS + 1)
        cv.setTrackbarPos("Max Sat", self.WINDOW1, self.maxS)

    def onMaxVTrackbar(self,val):
        self.maxV = max(val, self.minV + 1)
        cv.setTrackbarPos("Max Val", self.WINDOW1, self.maxV)

    def window_create(self):
        # Create windows
        cv.namedWindow(self.WINDOW1)
        cv.namedWindow(self.WINDOW2)

        # Create trackbars
        cv.createTrackbar("Min Hue", self.WINDOW1, self.minH, 180, self.onMinHTrackbar)
        cv.createTrackbar("Max Hue", self.WINDOW1, self.maxH, 180, self.onMaxHTrackbar)
        cv.createTrackbar("Min Sat", self.WINDOW1, self.minS, 255, self.onMinSTrackbar)
        cv.createTrackbar("Max Sat", self.WINDOW1, self.maxS, 255, self.onMaxSTrackbar)
        cv.createTrackbar("Min Val", self.WINDOW1, self.minV, 255, self.onMinVTrackbar)
        cv.createTrackbar("Max Val", self.WINDOW1, self.maxV, 255, self.onMaxVTrackbar)




fps, prev = 0.0, 0.0
cm = Camera()
while True:
    # Calculate FPS
    now = time.time()
    fps = (fps*FPS_SMOOTHING + (1/(now - prev))*(1.0 - FPS_SMOOTHING))
    prev = now

    # Get a frame
    frame = cm.read()

    # Blob detection works better in the HSV color space
    # (than the RGB color space) so the frame is converted to HSV.
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Create a mask using the given HSV range
    mask = cv.inRange(frame_hsv, (cm.minH, cm.minS, cm.minV), (cm.maxH, cm.maxS, cm.maxV))

    # Run the SimpleBlobDetector on the mask.
    # The results are stored in a vector of 'KeyPoint' objects,
    # which describe the location and size of the blobs.
    keypoints = detector.detect(mask)

    # For each detected blob, draw a circle on the frame
    frame_with_keypoints = cv.drawKeypoints(frame, keypoints, None, color = (0, 255, 0), flags = cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Write text onto the frame
    cv.putText(frame_with_keypoints, "FPS: {:.1f}".format(fps), (5, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    cv.putText(frame_with_keypoints, "{} blobs".format(len(keypoints)), (5, 35), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))

    # Display the frame
    cv.imshow(cm.WINDOW1, mask)
    cv.imshow(cm.WINDOW2, frame_with_keypoints)

    # Check for user input
    c = cv.waitKey(1)
    if c == 27 or c == ord('q') or c == ord('Q'): # Esc or Q
        camera.stop()
        break

camera.stop()
