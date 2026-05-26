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

# Initialize the EV3 Brick.            
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
cage = Motor(Port.C)
shooter = Motor(Port.D)

# # Initialize the drive base.
# robot = DriveBase(left_motor, right_motor, wheel_diameter=54, axle_track=150)

def motor_steering(speed, steer):
    if steer > 0: 
        left_motor.run(speed) 
        right_motor.run(speed - steer * speed / 50) 
    else: 
        left_motor.run(speed + steer * speed / 50) 
        right_motor.run(speed) 

# Play a sound.
ev3.speaker.beep()

# cage.run(400)
# time.sleep(4)
shooter.run_angle(500, -360)
# cage.run(400)
# time.sleep(1)
# motor_steering(600, 0)
# time.sleep(1)
# motor_steering(0,0)
# time.sleep(1)
# motor_steering(-600, 0)
# time.sleep(1)
# motor_steering(0,0)

# Play another beep sound.
ev3.speaker.beep(frequency=1000, duration=500)

#state = "search"
#while True:
    # read gyro
    # read open mv cam
    #int seeBall = 0
   # if state == "search":
       # if seeBall = 0:
          #  state = "chase"
    #elif state == "chase":
       # error = 1

