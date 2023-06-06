from math import sin, cos, pi
from pylx16a.lx16a import *
import time
from time import sleep
from sshkeyboard import listen_keyboard,stop_listening
LX16A.initialize("/dev/ttyUSB0")

# FLAGS
right_flag = False
left_flag = False
steering_flag = False
#mutexLock = False


# VARIABLES
theta = 0
motorSpeed = 500

# KEYBOARD LISTENER
def press(key):
		#print(f"'{key}' pressed")
	if key == 'w':
		motorSpeed = 100
		print("\nmotorSpeed=",motorSpeed)

	if key == 'a':
		theta = -45
		print("\ntheta=",theta)
		#stop_listening()

	if key == 'd':
		theta = 45
		print("\ntheta=",theta)

	if key == 's':
		motorSpeed = -100
		print("\nmotorSpeed=",motorSpeed)

listen_keyboard(on_press=press,)

# MANUAL INPUT
#motorSpeed = 300
#motorSpeed = input(f"motorspeed:\n")
#motorSpeed = int(motorSpeed)

# INITIALIZE SERVOS
try:
	servo1 = LX16A(1)  	# right front drive
	servo2 = LX16A(2)  	# right front steering
	servo3 = LX16A(3)  	# side drive
	servo4 = LX16A(4) 	# right back steering
	servo5 = LX16A(5)  	# right back drive
	servo6 = LX16A(6)  	# left front drive
	servo7 = LX16A(7)  	# left front steering
	servo8 = LX16A(8)  	# left drive
	servo9 = LX16A(9)  	# right back steering
	servo10 = LX16A(10) 	# right back drive
	#servo11 = LX16A(11) 	# backup

except ServoTimeoutError as e:
	print(f"Servo {e.id_} is not responding. Exiting...")
	quit()


# START YO ENGINES
#try:
while True:
	if right_flag == True:
		servo1.motor_mode(motorSpeed)
		servo3.motor_mode(motorSpeed)
		servo5.motor_mode(motorSpeed)

	if left_flag == True:
		servo6.motor_mode(motorSpeed)
		servo8.motor_mode(motorSpeed)
		servo10.motor_mode(motorSpeed)
# INTERRUPT
try:
    while True:
        sleep(0.5)

except KeyboardInterrupt:
	print('\nInterrupted!')

	# Stop all servos
	servo1.motor_mode(0)
	servo3.motor_mode(0)
	servo5.motor_mode(0)
	servo6.motor_mode(0)
	servo8.motor_mode(0)
	servo10.motor_mode(0)
	quit()




# STEERING
#theta= 0
#theta_right = 120-theta
#theta_left = 120+theta

while True:
	# CONSTRAIN SERVO ANGLES
	servo2.set_angle_limits(0,240)
        servo4.set_angle_limits(0,240)
        servo7.set_angle_limits(0,240)
        servo9.set_angle_limits(0,240)
	#servo11.set_angle_limits(0,240)		# backup servo

	if steering_flag == True
		servo2.move(theta_right)
        	servo4.move(theta_right)
        	servo7.move(theta_left)
        	servo9.move(theta_left)
		#servo11.move(theta_right)
