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
gyro = GyroSensor(Port.S4)

wheelRadius = 5.4 # milimeters

# setting up usb commands

fd = os.open('/dev/ttyACM0', os.O_RDONLY)

p = select.poll()
p.register(fd, select.POLLIN)

buf = b''

# initialise variables
ball_x = -1
ball_y = -1
GAIN = 1 #ange this accordingly 

robot_x = 220
robot_y = 100
prev_L = 0
prev_R = 0
# bigger quadrant
quadrant_x = 571.5
quadrant_y = 1181
#smaller quadrant
# quadrant_y = 881

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
    wheelCircumference = 17.6
    left_motor.reset_angle(0)
    while (left_motor.angle() / 360 * wheelCircumference < distance):
        motor_steering(speed, steer)
    motor_steering(0,0)

def spinnn(speed):
    left_motor.run(speed)
    right_motor.run(-1*speed)

def move_straight(speed):
    err =  gyro.angle() % 360 - 0
    corr = GAIN * err
    motor_steering(speed, corr)

def odometry():
    global robot_x, robot_y, prev_L, prev_R
    Ldeg = left_motor.angle() - prev_L
    Rdeg = right_motor.angle() - prev_R
    prev_L = left_motor.angle()
    prev_R = right_motor.angle()
    avg = (Ldeg + Rdeg) / 2
    avg = avg / 360 * 17.6
    gyro_angle = 90 - gyro.angle() 
    robot_x += avg * math.cos(math.radians(gyro_angle))
    robot_y += avg * math.sin(math.radians(gyro_angle))
    if ball_y != -1:
        ball_distance = 9583863 + (8.707394 - 9583863)/(1 + (ball_y/132649.3)**2.09492)
        print("ball distance: " + str(ball_distance))
        ball_field_x = robot_x + ball_distance * math.cos(math.radians(gyro_angle))
        ball_field_y = robot_y + ball_distance * math.sin(math.radians(gyro_angle))

#----------------
# EXECUTABLE CODE 
#----------------

counter = 0
shooter_counter = 0
state = "search"
gyro.reset_angle(0)
# motor_steering_dist(7, 500, 0)
# motor_steering(0, 0)
# while True:
#     read()
#     print('ball', ball_x, ball_y)
#     if ball_y != -1:
#         err = 217 - ball_x
#         corr = GAIN * err
#         motor_steering(500, corr)
#     else:
#         spinnn(200)
robot_number = 1

if robot_number == 1:     
    while True:
        # read gyro
        print(state)
        read()
        print('ball', ball_x, ball_y)
        print('heading', gyro.angle() % 360)
        odometry()
        if state == "search":
            spinnn(250)
            if ball_y != -1:
                state = "chase"
                motor_steering(0, 0)
                time.sleep(1)
                if counter == 0:
                    cage.run_angle(300, 90, wait=False)
                    counter = 1
        if state == "chase":
            err = 217 - ball_x
            corr = GAIN * err
            motor_steering(600, corr)
            print("motors are moving")
            if counter == 1:
                print("testing")
                if shooter_counter == 0:
                    shooter.run_angle(500, -250, wait = False)
                    shooter_counter == 1
                print("everything is working")
                counter = 2
            if ball_y == -1:
                state = "search"
            elif ball_y < 25:# to determine this through measurement of the camera FOV
                state = "capture"
            # continue
        elif state == "capture":
            if counter == 2:
                motor_steering(900, 0)
                #time.sleep(0.5)
                cage.run_angle(300, -90, wait=True)
                counter = 3




                
            #t without crossing the red line 
            #-----pseudo code-----
            # while red ramp not within view:
            # drive forward
            # else:
            # turn to face the opposing wall (minimise launching distance)
            # shoot the ball over the wall
            # verify that the ball is not in # eventuallyp need to add method of verification for this - when the ball enters 
            # the shooting zone, return something verifying this during this step 
            if ball_y < 24:
                state = "aim"
            continue
        elif state == "aim":
            spinnn(300)
            # cage.run_angle(300, 90, wait=False)
            if gyro.angle() % 360 < 3 or gyro.angle() % 360 >353:
                motor_steering_dist(0.5, 700, 0)
                state = "shoot"
        elif state == "shoot":
            # locate the ramp
            # shoot within capture area
            if shooter_counter == 1:
                shooter.run_angle(500, -110, wait = True)
                print("heidi")
                shooter_counter = 0
            # if True:
            break
        prev_L = left_motor.angle()
        prev_R = right_motor.angle()
    print(gyro.angle())
    motor_steering(0, 0)

else:
    while True:
        # read gyro
        print(state)
        read()
        print('ball', ball_x, ball_y)
        print('heading', gyro.angle() % 360)
        odometry()
        if state == "search":
            spinnn(250)
            if ball_y != -1:
                state = "chase"
                motor_steering(0, 0)
                time.sleep(1)
                if counter == 0:
                    cage.run_angle(300, 90, wait=False)
                    counter = 1
        if state == "chase":
            err = 217 - ball_x
            corr = GAIN * err
            motor_steering(600, corr)
            print("motors are moving")
            if counter == 1:
                print("testing")
                if shooter_counter == 0:
                    shooter.run_angle(500, -250, wait = False)
                    shooter_counter == 1
                print("everything is working")
                counter = 2
            if ball_y == -1:
                state = "search"
            elif ball_y < 25:# to determine this through measurement of the camera FOV
                state = "capture"
            # continue
        elif state == "capture":
            if counter == 2:
                motor_steering(900, 0)
                #time.sleep(0.5)
                cage.run_angle(300, -90, wait=True)
                counter = 3




                
            #t without crossing the red line 
            #-----pseudo code-----
            # while red ramp not within view:
            # drive forward
            # else:
            # turn to face the opposing wall (minimise launching distance)
            # shoot the ball over the wall
            # verify that the ball is not in # eventuallyp need to add method of verification for this - when the ball enters 
            # the shooting zone, return something verifying this during this step 
            if ball_y < 24:
                state = "aim"
            continue
        elif state == "aim":
            spinnn(300)
            # cage.run_angle(300, 90, wait=False)
            if gyro.angle() % 360 < 3 or gyro.angle() % 360 >353:
                motor_steering_dist(0.5, 700, 0)
                state = "shoot"
        elif state == "shoot":
            # locate the ramp
            # shoot within capture area
            if shooter_counter == 1:
                shooter.run_angle(500, -110, wait = True)
                print("heidi")
                shooter_counter = 0
            # if True:
            break
        prev_L = left_motor.angle()
        prev_R = right_motor.angle()
    print(gyro.angle())
    motor_steering(0, 0)
