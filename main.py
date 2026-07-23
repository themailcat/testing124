!/usr/bin/env pybricks micro-python
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

# Initialize the EV3 Brick.            
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
cage = Motor(Port.C)
shooter = Motor(Port.D)

wheelRadius = 5.4 # milimeters

# # Initialize the drive base.
# robot = DriveBase(left_motor, right_motor, wheel_diameter=54, axle_track=150)

# Set baudrate in Python
# os.system() runs the specified command
# You can also run the "stty" command from the commandline.


import os
import select
# List files in the current working directory

# Open the /dev/ttyUSB0 file in read only mode. This file represents the serial device
# Depending on your serial device, the filename may change (eg. /dev/ttyACM0)
fd = os.open('/dev/ttyACM0', os.O_RDONLY)

# Create a select object and register the previously opened file in input (reading) mode
# This let us check if there is data available for reading from the file.
p = select.poll()
p.register(fd, select.POLLIN)

# Create an empty bytes object to receive data from the file
buf = b''

x = 0
y = 0

# Read from serial
def read():
    global buf, x, y

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
        string = buf_copy.decode()

        # If you have multiple values in each line, split the string
        # Here we split by comma, but use whatever is suitable for your data
        values = string.split(',')

        # # Convert your values from string to numbers
        x = values[0]
        y = values[1]
    except:
        pass

# Retrieve the last read value
def get():
    return x, y

# Read and discard all data from buffer.
# If the EV3 is unable to read from serial for a while, you should run this to clear the read
# buffer, else the EV3 may take a while to process all the buffered data.
def clear():
    while p.poll(0):
        os.read(fd, 100)


#########################
# Main loop for testing #
#########################

import time
timeout = 0

while True:
    read()

    # We read every loop, but prints only once per second.
    now = time.time()
    if now > timeout:
        timeout = now + 1
        print(get())

def motor_steering(speed, steer):
    if steer > 0: 
        left_motor.run(speed) 
        right_motor.run(speed - steer * speed / 50) 
    else: 
        left_motor.run(speed + steer * speed / 50) 
        right_motor.run(speed) 

def motor_steering_dist(distance, speed, steer):
    wheelCircumference = wheelRadius * 2 * math.pi
    left_motor.reset_angle(0)
    current_angle = left_motor.angle()
    while (current_angle / 360 * wheelCircumference < distance):
        motor_steering(speed, steer)
    motor_steering(0, 0)

# Play a sound.
ev3.speaker.beep()

cage.run(400)
time.sleep(4)
cage.run(400)
time.sleep(1)
shooter.run_angle(500, -300)
motor_steering_dist(10, 500, 0)
cage.run_angle(300, 90)
motor_steering(400, 0)
time.sleep(1)
motor_steering(0, 0)
motor_steering_dist(3, 500, 0)
shooter.run_angle(500, -60)
motor_steering(0,0)
time.sleep(1)
motor_steering(-600, 0)
time.sleep(1)
motor_steering(0,0)

# Play another beep sound.
ev3.speaker.beep(frequency=1000, duration=500)

state = "search"
while True:
    # read gyro
    # read open mv cam
    int seeBall = 0
   if state == "search":
       if seeBall = 0:
           state = "chase"
    elif state == "chase":
       error = 1

print(my_ev3.list_dir('/dev/ttyACM0'))