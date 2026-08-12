#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                   InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time 
import math 
import os
import select

# Initialize the EV3 Brick.            
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
cage = Motor(Port.C)
shooter = Motor(Port.D)

wheelRadius = 5.4 # milimeters

# setting up usb commands

fd = os.open('/dev/ttyACM0', os.O_RDONLY)

p = select.poll()
p.register(fd, select.POLLIN)

buf = b''

# initialise variables
ball_x = -1
ball_y = -1
GAIN = 2# change this accordingly 

# Read from serial
def read():
    global buf, ball_x, ball_y

    # Loop as long as data is available
    # p.poll() will return None if no data is available
    # Note that the "0" is the timeout duration
    # If absent, the poll() command will wait until data is available
    while p.poll(0):

        # Since data is available, we can safely read from the file without blocking
        char = os.read(fd, 1) # read one byte
        
        # Check if it's a newline character
        if char != b'\n':
            # If the char is not a newline, that means you have not reached the end of the line.
            # Add the character to the buffer
            buf += char
        else:
            # If it's a newline, make a copy of it, then empty buf
            # Checking that the len is greater than 0 is to prevent empty lines from being processed
            if len(buf) > 0:
                buf_copy = buf
                buf = b''

    # Exited from loop. That means we have read everything.
    # buf_copy should contain the last full line and we can process it

    # The "try/except" is to protect against errors. If the data is corrupted,
    # the conversion may fail. Without the try/except, your program will terminate
    # immediately. With try/except, your program will catch the error and do a
    # "pass" (ie. nothing)
    try:
        # First decode the bytes into a string
        values = buf_copy.decode()
        

        # If you have multiple values in each line, split the string
        # Here we split by comma, but use whatever is suitable for your data
        if values == -1:
            ball_y = -1
        else:
            values = values.split(',')
            # # Convert your values from string to numbers
            ball_y = int(values[0])
            ball_x = int(values[1])
            
    except:
        pass

# Retrieve the last read value
def get():
    return ball_x, ball_y

# Read and discard all data from buffer.
# If the EV3 is unable to read from serial for a while, you should run this to clear the read
# buffer, else the EV3 may take a while to process all the buffered data.
def clear():
    while p.poll(0):
        os.read(fd, 100)

# import time
# timeout = 0

# while True:
#     read()

#     # We read every loop, but prints only once per second.
#     now = time.time()
#     if now > timeout:
#         timeout = now + 1
#         print(get())

def motor_steering(speed, steer):
    if steer > 0: 
        left_motor.run(speed) 
        if speed != 0:
            print("left motor speed:"+ str(speed))
        right_motor.run(speed - steer * speed / 50) 
        if speed != 0:
            print("right motor speed:"+ str(speed - steer * speed / 50))
    else: 
        left_motor.run(speed + steer * speed / 50) 
        if speed != 0:
            print("left motor speed:"+ str(speed + steer * speed / 50))
        right_motor.run(speed)
        if speed != 0:
            print("right motor speed:"+ str(speed))

def motor_steering_dist(distance, speed, steer):
    wheelCircumference = wheelRadius * 2 * math.pi
    left_motor.reset_angle(0)
    current_angle = left_motor.angle()
    while (current_angle / 360 * wheelCircumference < distance):
        motor_steering(speed, steer)
    motor_steering(0, 0)

def spinnn(speed):
    left_motor.run(speed)
    right_motor.run(-1*speed)

#----------------
# EXECUTABLE CODE 
#----------------
counter = 0
state = "search"
while True:
    # read gyro
    print(state)
    read()
    print(ball_y)
    if state == "search":
        spinnn(400)
        if ball_y != -1:
            state = "chase"
            motor_steering(0, 0)
            if state == "search":
                print("WARNING: state did not change: chase")
            if counter == 0:
                cage.run_angle(300, 90, wait=False)
                counter = 1
        continue
    elif state == "chase":
        err = 160 - ball_x
        corr = GAIN * err
        motor_steering(600, corr)
        print("motors are moving")
        if counter == 1:
            print("testing")
            shooter.run_angle(500, -300, wait=False)
            print("everything is working")
            counter = 2
        if ball_y == -1:
            state = "search"
        elif ball_y > 250: # need to determine this through measurement of the camera FOV
            state = "capture"
        continue
    elif state == "capture":
        motor_steering(0, 0)
        if counter == 2:
            cage.run_angle(300, -90, wait=False)
            counter = 3
        #t without crossing the red line 
        #-----pseudo code-----
        # while red ramp not within view:
        # drive forward
        # else:
        # turn to face the opposing wall (minimise launching distance)
        # shoot the ball over the wall
        # verify that the ball is not in # eventually need to add method of verification for this - when the ball enters 
        # the shooting zone, return something verifying this during this step 
        if ball_y > 250:
            state = "shoot"
        continue
    elif state == "shoot":
        # locate the ramp
        # shoot within capture area
        time.sleep(1)
        shooter.run_angle(500, -70, wait=True)
        # if True:
        break
motor_steering(0, 0)