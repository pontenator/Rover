from math import sin, cos, pi
from pylx16a.lx16a import *
import time
from time import sleep
from sshkeyboard import listen_keyboard,stop_listening
import keyboard

# Initialize the LX-16A library @ ttyUSB0
LX16A.initialize("/dev/ttyUSB0")

# GLOBAL SCOPE
motorSpeed = 0

# Keyboard listener
async def press(key):
	global motorSpeed, theta

	if key == 'right':
		theta -= 20
	elif key == "left":
		theta += 20
	elif key == "up":
		motorSpeed += 100
	elif key == "down":
		motorSpeed -= 100

	print(f"motorSpeed: {motorSpeed}, theta: {theta}")

	driveRF.motor_mode(-motorSpeed)
	driveR.motor_mode(-motorSpeed)
	driveRB.motor_mode(-motorSpeed)

	driveLF.motor_mode(motorSpeed)
	driveL.motor_mode(motorSpeed)
	driveLB.motor_mode(motorSpeed)

	steerLF.move(140-theta)		# 150	_right	OK
	steerRF.move(165-theta)		# 165	_right	OK
	steerLB.move(140+theta)		# 140	_left	OK
	steerRB.move(125+theta)		# 125	_left	OK


async def release(key):
#	print(f"'{key}' released")
	pass

# Initialize servos
try:
	driveRF = LX16A(1)
	steerRF = LX16A(2)
	driveR = LX16A(3)
	steerRB = LX16A(4)
	driveRB = LX16A(5)

	driveLF = LX16A(6)
	steerLF = LX16A(7)
	driveL = LX16A(8)
	steerLB = LX16A(9)
	driveLB = LX16A(10)

	steerRF.set_angle_limits(0,240)
	steerRB.set_angle_limits(0,240)
	steerLF.set_angle_limits(0,240)
	steerLB.set_angle_limits(0,240)

except ServoTimeoutError as e:
	print(f"Servo {e.id_} is not responding. Exiting...")
	quit()

theta = 0
thetaFront = 120
thetaBack = 140

### Main loop
try:
	listen_keyboard(
		on_press=press,
		on_release=release,
	)

### INTERRUPT
except KeyboardInterrupt:
	print('\nInterrupted!')

	# Stop all servos
	driveRF.motor_mode(0)
	driveR.motor_mode(0)
	driveRB.motor_mode(0)

	driveLF.motor_mode(0)
	driveL.motor_mode(0)
	driveLB.motor_mode(0)
#	quit()
