from math import sin, cos, pi
from pylx16a.lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0")

id = 0
while not id:
    try:
        text = input(f"Connect servo, and input id [1-11]. Press enter to continue\n")

        text = int(text)

        if text > 0 and text < 12:
            id = text
    except:
        pass

servo = None
for old_id in range(1, 12):
    print(f"Testing id {old_id}")
    try:
        servo = LX16A(old_id)
        break
    except ServoTimeoutError as e:
        pass

if not servo:
    print("Unable to connect to servo. Retry")
    exit()

print(f"Found servo with id {old_id}. Changing to id {id}")

servo.set_id(id)

for t in range(0, 11):
    servo.move(sin(t * 0.1) * 60 + 60)
    time.sleep(0.05)

