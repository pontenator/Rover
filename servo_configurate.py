from math import sin, cos, pi
from pylx16a.lx16a import *
import time

# Initialize the LX-16A library @ ttyUSB0
LX16A.initialize("/dev/ttyUSB0")

id = 0
while not id:
    try:
        # User input
        text = input(f"Connect servo, and input id [1-11]. Press enter to continue\n")
        # Convert to integer
        text = int(text)

        # Check if input is in range
        if text > 0 and text < 12:
            id = text
    except:
        pass

# Interate until a valid servo ID is found
servo = None
for old_id in range(1, 12):
    print(f"Testing id {old_id}")
    try:
        # Create an LX16A object for the current ID
        servo = LX16A(old_id)
        break
    except ServoTimeoutError as e:
        pass

# If servo was not found
if not servo:
    print("Unable to connect to servo. Retry")
    exit()

# If servo was found
print(f"Found servo with id {old_id}. Changing to id {id}")

# Set the servo ID
servo.set_id(id)

# Run the servo
for t in range(0, 11):
    servo.move(sin(t * 0.1) * 60 + 60)
    time.sleep(0.05)

