from math import sin, cos, pi
from pylx16a.lx16a import *
import time
from time import sleep
from sshkeyboard import listen_keyboard,stop_listening
import pygame
import math


for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        syspath="${sysdevpath%/dev}"
        devname="$(udevadm info -q name -p $syspath)"
        [[ "$devname" == "bus/"* ]] && exit
        eval "$(udevadm info -q property --export -p $syspath)"
        [[ -z "$ID_SERIAL" ]] && exit
        echo "/dev/$devname - $ID_SERIAL"
    )
done

LX16A.initialize("/dev/ttyUSB0")

# Flags
right_flag = False
left_flag = False
steering_flag = False
xbox_flag = False
mutexLock = False

## Constants
turn_radius = 0
wheelbase = 0
steering_angle = 0
motorSpeedMax = 1000

## Ackermann stearing
def calculate_steering_angle(turn_radius, wheelbase):
    """
    Calculate the steering angle for Ackermann steering geometry.

    Args:
        turn_radius (float): Desired turn radius of the vehicle.
        wheelbase (float): Distance between the front and rear axles.

    Returns:
        float: Steering angle in radians.
    """
    return math.atan(wheelbase / turn_radius)

def calculate_inner_wheel_angle(steering_angle, wheelbase):
    """
    Calculate the inner wheel angle for Ackermann steering geometry.

    Args:
        steering_angle (float): Steering angle in radians.
        wheelbase (float): Distance between the front and rear axles.

    Returns:
        float: Inner wheel angle in radians.
    """
    return math.atan(2 * wheelbase * math.sin(steering_angle) / wheelbase)

def calculate_outer_wheel_angle(steering_angle, wheelbase):
    """
    Calculate the outer wheel angle for Ackermann steering geometry.

    Args:
        steering_angle (float): Steering angle in radians.
        wheelbase (float): Distance between the front and rear axles.

    Returns:
        float: Outer wheel angle in radians.
    """
    return math.atan(2 * wheelbase * math.sin(steering_angle) / wheelbase) + steering_angle

# Initialize servos
try:
	driveRF = LX16A(1)  	# right front drive
	steerRF = LX16A(2)  	# right front steering
	steerRF.set_angle_limits(0,240)
	driveR = LX16A(3)  	    # side drive
	steerRB = LX16A(4) 	    # right back steering
    steerRB.set_angle_limits(0,240)
	driveRB = LX16A(5)  	# right back drive
	
    driveLF = LX16A(6)  	# left front drive
	steerLF = LX16A(7)  	# left front steering
    steerLF.set_angle_limits(0,240)
	driveL = LX16A(8)  	    # left drive
	steerLB = LX16A(9)  	# right back steering
    steerLB.set_angle_limits(0,240)
    driveLB = LX16A(10) 	# right back drive
    #servo11 = LX16A(11) 	# backup
    #servo11.set_angle_limits(0,240)		# backup servo
    # CONSTRAIN SERVO ANGLES

except ServoTimeoutError as e:
	print(f"Servo {e.id_} is not responding. Exiting...")
	quit()


if xbox_flag == True:
    # Initialize pygame
    pygame.init()
    pygame.joystick.init()

    # Check for connected controllers
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("No xbox controller found...")
        exit()
	
if xbox_flag == False:
    theta = 0     # Manual input
    #motorSpeed = input(f"motorspeed:\n")
    #motorSpeed = int(motorSpeed)



# Main loop
try:
    while True:
    	if right_flag == True:
	    	driveRF.motor_mode(motorSpeed)
		    driveR.motor_mode(motorSpeed)
		    driveRB.motor_mode(motorSpeed)

	    if left_flag == True:
    		driveLF.motor_mode(motorSpeed)
	    	driveL.motor_mode(motorSpeed)
    		driveLB.motor_mode(motorSpeed)
    	
        ##Steering
        if steering_flag == True:
	    	steerRF.move(theta_right)
            steerLF.move(theta_right)
        	steerRB.move(theta_left)
        	steerRB.move(theta_left)
		    #servo11.move(theta_right)

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

finally:
	print('\nMade it to finally')
    # Clean up



# STEERING
#theta= 0
#theta_right = 120-theta
#theta_left = 120+theta
