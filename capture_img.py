from picamera2 import Picamera2, MappedArray
import cv2 as cv
import numpy as np
import time

thisThing  = True
pic_folder = "/home/pnut/cv/scripts/picz/"

# Initialize Picamera2 instances for both cameras
camera_left = Picamera2(0)
camera_right = Picamera2(1)

# Configure cameras
RESOLUTION = (640, 480)
#RESOLUTION = (1456, 1088)
config_left = camera_left.create_preview_configuration(main={"size": RESOLUTION})
config_right = camera_right.create_preview_configuration(main={"size": RESOLUTION})

camera_left.configure(config_left)
camera_right.configure(config_right)

# Start cameras
camera_left.start()
camera_right.start()

time.sleep(2)


# Capture frames from both cameras
frame_left = camera_left.capture_array()
frame_right = camera_right.capture_array()

cv.namedWindow('output', cv.WINDOW_AUTOSIZE)
cv.imshow('output', frame_left)


cv.imwrite(f"{pic_folder}/frame_left.jpg", frame_left)
cv.imwrite(f"{pic_folder}/frame_right.jpg", frame_right)


# Break the loop on 'q' key press
#if cv.waitKey(1) & 0xFF == ord('q'):
#    break

# Stop cameras
camera_left.stop()
camera_right.stop()

cv.destroyAllWindows()
print("end of script")