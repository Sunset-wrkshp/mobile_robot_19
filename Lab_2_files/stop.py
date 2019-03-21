# Stops the robot

from encoder_class import Encoder
import RPi.GPIO as GPIO

print("Forced Stop")
d = Encoder()
d.stop()
GPIO.cleanup()
exit()
