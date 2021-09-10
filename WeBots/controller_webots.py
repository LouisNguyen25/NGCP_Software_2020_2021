from controller import Robot, Camera, CameraRecognitionObject
from controller import Keyboard, Gyro, Accelerometer, Compass
import time


def forward(topMotor) :
    topMotor.setVelocity(1.0)

def backward(topMotor) :
    topMotor.setVelocity(-1.0)
    
def stop(topMotor) :
    topMotor.setVelocity(0.0)


TIME_STEP = 64
UPRIGHT_THRESH = 4.9

robot = Robot()

camera = Camera("CAM")
camera = robot.getDevice("CAM")
camera.enable(TIME_STEP)
camera2 = Camera("CAM2")
camera2 = robot.getDevice("CAM2")
camera2.enable(TIME_STEP)
camera.recognitionEnable(TIME_STEP)
camera2.recognitionEnable(TIME_STEP)
################### MPU-9250 for Embedded Below #################
accel = Accelerometer("ACC")
accel.enable(TIME_STEP)
compass = robot.getDevice("COMPASS")
compass.enable(TIME_STEP)
gyro = robot.getDevice("GYRO")
gyro.enable(TIME_STEP)

wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getDevice(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
avoidObstacleCounter = 0

topMotor = robot.getDevice('topMotor')
topMotor.setPosition(float('inf'))
topMotor.setVelocity(0.0)

keyboard = Keyboard() # keyboard object
keyboard.enable(TIME_STEP) # enable keyboard object for input

yAxis = 0
yAxisPrev = 0
counter = 10
numberOfLanded = 0
landed = False
while robot.step(TIME_STEP) != -1:

    print("Gyro: ", gyro.getValues())

    print("Compass: ", compass.getValues())
    
    print("Accel: ", accel.getValues())
 
    yAxisPrev = yAxis
    xAxis, yAxis, zAxis = accel.getValues()

# For "green light" after landing 
    if yAxis > UPRIGHT_THRESH :
        if abs(yAxis - yAxisPrev) < 0.01 and not landed:
            numberOfLanded += 1
            yAxisPrev = yAxis
    else :
        print("NOT UPRIGHT")
        landed = False
        
        
    print("Upright checks: ", numberOfLanded)
    if numberOfLanded >= counter and not landed :   
        print("Upright")
        landed = True
        numberOfLanded = 0
        
    if(landed) :
        leftSpeed = 2.5
        rightSpeed = 2.5

    else :
        leftSpeed = 0
        rightSpeed = 0

    input = keyboard.getKey()
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)
    if(input == 315) : # top arrow
        forward(topMotor)
    elif(input == 317) : # down arrow
        backward(topMotor)
    else :
        stop(topMotor)