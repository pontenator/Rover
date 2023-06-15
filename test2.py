from math import sin, cos, pi
from pylx16a.lx16a import *
import time
from time import sleep
from sshkeyboard import listen_keyboard,stop_listening
LX16A.initialize("/dev/ttyUSB0")

### FLAGS
right_flag = True
left_flag = True
steering_flag = False
xbox_flag = False
#mutexLock = False

### Constants
turn_radius = 0
wheelbase = 0
steering_angle = 0
motorSpeedMax = 1000

### VARIABLES
theta = 0
theta_right = 120-theta
theta_left = 120+theta
motorSpeed = 500

### KEYBOARD LISTENER
#def press(key):
#	if manual_flag == False:
		#print(f"'{key}' pressed")
#		if key == 'w':
#			motorSpeed = 100
			#print("\nmotorSpeed=",motorSpeed)

#		if key == 'a':
#			theta = -45
			#print("\ntheta=",theta)

#		if key == 'd':
#			theta = 45
			#print("\ntheta=",theta)

#		if key == 's':
#			motorSpeed = -100
#			print("\nmotorSpeed=",motorSpeed)

#	listen_keyboard(on_press=press,)

### MANUAL INPUT
#if manual_flag == True:
#	motorSpeed = 300
	#motorSpeed = input(f"motorspeed:\n")
	#motorSpeed = int(motorSpeed)

#if xbox_flag == True:
    	# Initialize pygame
#	pygame.init()
#	pygame.joystick.init()

    	# Check for connected controllers
#	joystick_count = pygame.joystick.get_count()
#	if joystick_count == 0:
#		print("No xbox controller found...")
#		exit()

#if xbox_flag == False:
    #theta = 0     # Manual input
    #motorSpeed = input(f"motorspeed:\n")
    #motorSpeed = int(motorSpeed)


## Ackermann stearing
#def calculate_steering_angle(turn_radius, wheelbase):
#    return math.atan(wheelbase / turn_radius)

#def calculate_inner_wheel_angle(steering_angle, wheelbase):
#    return math.atan(2 * wheelbase * math.sin(steering_angle) / wheelbase)

#def calculate_outer_wheel_angle(steering_angle, wheelbase):
#    return math.atan(2 * wheelbase * math.sin(steering_angle) / wheelbase) + steering_angle


##############################################


# Initialize servos
try:

#	if right_flag == True:
		driveRF = LX16A(1)
		steerRF = LX16A(2)
		driveR = LX16A(3)
		steerRB = LX16A(4)
		driveRB = LX16A(5)

#	if left_flag == True:
		driveLF = LX16A(6)
		steerLF = LX16A(7)
		driveL = LX16A(8)
		steerLB = LX16A(9)
		driveLB = LX16A(10)

#	if steering_flag == True:
		steerRF.set_angle_limits(0,240)
		steerRB.set_angle_limits(0,240)
		steerLF.set_angle_limits(0,240)
		steerLB.set_angle_limits(0,240)

except ServoTimeoutError as e:
	print(f"Servo {e.id_} is not responding. Exiting...")
	quit()




### Main loop
try:
	while True:
		if right_flag == True:
			driveRF.motor_mode(motorSpeed)
			driveR.motor_mode(motorSpeed)
			driveRB.motor_mode(motorSpeed)
		if left_flag == True:
			driveLF.motor_mode(-motorSpeed)
			driveL.motor_mode(-motorSpeed)
			driveLB.motor_mode(-motorSpeed)

	#	if steering_flag == True:
	#		steerLF.move(theta) 		#_right
	#		steerRF.move(theta) 		#_right
	#		steerLB.move(theta)  		#_left
	#		steerLB.move(theta)		#_left




### INTERRUPT
except KeyboardInterrupt:
	print('\nInterrupted!')
	quit()
	# Stop all servos
#	driveRF.motor_mode(0)
#	driveR.motor_mode(0)
#	driveRB.motor_mode(0)

#	driveLF.motor_mode(0)
#	driveL.motor_mode(0)
#	driveLB.motor_mode(0)
#	quit()
