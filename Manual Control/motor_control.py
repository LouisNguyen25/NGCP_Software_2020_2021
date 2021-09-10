#!/bin/python3

import RPi.GPIO as GPIO
import time

Motor_A_EN = 24
Motor_B_EN = 25

pwm_A = 0
pwm_B = 0

def setup(): 
    global pwm_A, pwm_B

    # Disable Warnings for using pins 18/22 as Outputs
    GPIO.setwarnings(False)

    # Setup our pins to be read based on Broadcom SOC 
    GPIO.setmode(GPIO.BCM)

    # Setup Both Motor Channesl as Outputs
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
        
    # Create a PWM instance for Both Motors (Channel, Frequency)
    pause = 1/(2800 * 10**-6)
    pwm_A = GPIO.PWM(Motor_A_EN, pause)
    pwm_B = GPIO.PWM(Motor_B_EN, pause)
    pwm_A.start(50)
    pwm_B.start(50)
    print("completed setup\n")

# Manipulate the right motor
def motor_right(duty):  
    global pwm_B
    pwm_B.ChangeFrequency(duty)

# Manipulate the left motor
def motor_left(duty):   
    global pwm_A
    pwm_A.ChangeFrequency(duty)

def destroy():
    print("Ending Program")
    GPIO.cleanup()             # Release resource

# Accept UserInput for direction, percentage, and which wheel.
def percentage(motor, direction, percent):
    print("Converting from % to actual value")
    if motor == 0:
        if direction == 0:
            print("Clockwise Mode, at %{0}".format(percent))
            conversion = (2800 + (1000*percent*0.01))
            d = 1/(conversion*10**-6)
            motor_right(d)
        elif direction == 1: 
            print("Counter-Clockwise: %{0}".format(percent))        
            conversion = (2800 - (1000 *percent*0.01))
            d=1/(conversion*10**-6)
            motor_right(d)
        else:
            print("ERROR: Unsure which direction selected. Try Again.")
    elif motor == 1:
        if direction == 0:
            print("Clockwise Mode, at %{0}".format(percent))
            conversion = (2800 + (1000*percent*0.01))
            d = 1/(conversion*10**-6)
            motor_left(d)
        elif direction == 1: 
            print("Counter-Clockwise: %{0}".format(percent))        
            conversion = (2800 - (1000 *percent*0.01))
            d=1/(conversion*10**-6)
            motor_left(d)
        else:
            print("ERROR: Unsure which direction selected. Try Again.")
    elif motor == 2:
        if direction == 0:
            print("Clockwise Mode, at %{0}".format(percent))
            conversion = (2800 + (1000*percent*0.01))
            d = 1/(conversion*10**-6)
            motor_left(d)
            motor_right(d)
        elif direction == 1: 
            print("Counter-Clockwise: %{0}".format(percent))        
            conversion = (2800 - (1000 *percent*0.01))
            d=1/(conversion*10**-6)
            motor_left(d)
            motor_right(d)
        else:
            print("ERROR: Unsure which direction selected. Try Again.")
    else:
        print("ERROR: Unsure which motor selected. Try Again.")


print("NGCP MOTOR CONTROL SCRIPT")
setup()

try:
    while True:
        # motor = input('Please enter which motor you want to manipulate. Right motor "0", Left Motor "1", Both motors "2":\n')
        # direction = input('Please enter direction for motors to move in, either clockwise "0" or counter-clockwise "1":\n')
        # percent = input('Please enter percentage you want speed to run in, from 0 to 100 percent:\n')
        # try:
        #     m = int(motor)
        #     d = int(direction)
        #     p = float(percent)
        # except ValueError:
        #     print("ERROR: Please enter a valid input")
        #     continue
        # percentage(m,d,p)


        # if left:
        #     percentage(m,d,p)
        #     percentage(m,d,p)
        # elif right:
        #     percentage(m,d,p)
        #     percentage(m,d,p)
        # else: #straight
        #     percentage(m,d,p)

except KeyboardInterrupt:
    print("Exiting...")
    destroy()
