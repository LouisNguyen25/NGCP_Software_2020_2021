import pygame
from controller import Robot, Camera, CameraRecognitionObject
from controller import Keyboard, Gyro, Accelerometer, Compass
import time

MAX_SPEED = 8.0

def joystick_moved(value):
    # If joystick value is very small, likely that joystick is not being moved intentionally
    if abs(value) < .2:
        return False
    else:
        return True


class CurrentInput:
    """
    Class containing the most recent positional and camera joystick input made by user
    """
    def __init__(self):
        self.x_pos = 0.0
        self.y_pos = 0.0
        self.x_cam = 0.0
        self.y_cam = 0.0

    def update_movement_x(self, x):
        if joystick_moved(x):
            # Update value stored in the CurrentInput object to the value read from joystick input
            self.x_pos = round(x, 2)
            print("Updated movement x to: ", self.x_pos)  # FOR DEBUGGING
        else:
            # If joystick value is very small, update value stored in CurrentInput object to be 0
            self.x_pos = 0

    def update_movement_y(self, y):
        if joystick_moved(y):
            self.y_pos = round(y, 2)
            print("Updated movement y to: ", self.y_pos)  # FOR DEBUGGING
        else:
            self.y_pos = 0

    def update_camera_x(self, x):
        if joystick_moved(x):
            self.x_cam = round(x, 2)
            #print("Updated camera x to: ", self.x_cam)  # FOR DEBUGGING
        else:
            self.x_cam = 0

    def update_camera_y(self, y):
        if joystick_moved(y):
            self.y_cam = round(y, 2)
            #print("Updated camera y to: ", self.y_cam)  # FOR DEBUGGING
        else:
            self.y_cam = 0
           
    def get_x_pos(self) :
        return self.x_pos
        
    def get_y_pos(self) :
        return self.y_pos

"""=============== Mapping Algorithm =================="""
def move(joystick):

    x = joystick.get_x_pos()
    y = -joystick.get_y_pos() 
    
    # going forward
    if y >= 0:
        wheels[0].setVelocity((y + x) * MAX_SPEED)
        wheels[1].setVelocity((y - x) * MAX_SPEED)
        wheels[2].setVelocity((y + x) * MAX_SPEED)
        wheels[3].setVelocity((y - x) * MAX_SPEED)
    # going backward
    elif y < 0:
        wheels[0].setVelocity((y - x) * MAX_SPEED)
        wheels[1].setVelocity((y + x) * MAX_SPEED)
        wheels[2].setVelocity((y - x) * MAX_SPEED)
        wheels[3].setVelocity((y + x) * MAX_SPEED)

def forward(topMotor) :
    topMotor.setVelocity(1.0)

def backward(topMotor) :
    topMotor.setVelocity(-1.0)
    
def stop(topMotor) :
    topMotor.setVelocity(0.0)

def turnLeft(wheels):
    wheels[0].setVelocity(-1.0)
    wheels[1].setVelocity(1.0)
    wheels[2].setVelocity(-1.0)
    wheels[3].setVelocity(1.0)

def turnRight(wheels) :
    wheels[0].setVelocity(1.0)
    wheels[1].setVelocity(-1.0)
    wheels[2].setVelocity(1.0)
    wheels[3].setVelocity(-1.0)

def driveForward(wheels):
    wheels[0].setVelocity(1.0)
    wheels[1].setVelocity(1.0)
    wheels[2].setVelocity(1.0)
    wheels[3].setVelocity(1.0)

def driveBackward(wheels):
    wheels[0].setVelocity(-1.0)
    wheels[1].setVelocity(-1.0)
    wheels[2].setVelocity(-1.0)
    wheels[3].setVelocity(-1.0)

def idle(wheels):
    wheels[0].setVelocity(0.0)
    wheels[1].setVelocity(0.0)
    wheels[2].setVelocity(0.0)
    wheels[3].setVelocity(0.0)

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

# Init current input object
c = CurrentInput()

robot = Robot()
TIME_STEP = 64
UPRIGHT_THRESH = 4.9

# Main loop
while robot.step(TIME_STEP) != -1:
    # Need to process events for it to work
    for event in pygame.event.get():
        None

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for j in range(joystick_count):
        joystick = pygame.joystick.Joystick(j)
        joystick.init()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()

        # Usually axis run in pairs, up/down for one, and left/right for the other.
        axes = joystick.get_numaxes()

        continuousAxes = []

        for ax in range(axes):
            axis = joystick.get_axis(ax)

            #  Write to dataexport.txt
            continuousAxes.append(axis)
            #file_object = open("dataexport.txt", "a+")
            #file_object.write("{}\n".format(continuousAxes[0]))
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

            print("Axis X : ", c.get_x_pos())
            print("Axis Y : ", c.get_y_pos())
            
            # Get Values and multiply to wheel velocity
            
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
   
            
# =================== Joystick Input ====================
            move(c)


# =================== Keyboard Input ====================
            # input = keyboard.getKey()
            # if(input == 87 or input == 119):      # w
            #     driveForward(wheels)
            # elif(input == 97 or input == 65):     # a
            #     turnLeft(wheels)
            # elif(input == 83 or input == 115):    # s
            #     driveBackward(wheels)
            # elif(input == 68 or input == 100):    # d
            #     turnRight(wheels)
            # elif(input == 315) : # top arrow
            #     forward(topMotor)
            # elif(input == 317) : # down arrow
            #     backward(topMotor)
            # else :
            #     idle(wheels)
            #     stop(topMotor)

            print("ax value is : ", ax)
            #  Update left joystick horizontal axis (-1.0 for left, 1.0 for right)
            if ax == 0:
                c.update_movement_x(axis)
            #  Update left joystick vertical axis (-1.0 for up, 1.0 for down)
            if ax == 1:
                c.update_movement_y(axis)

            #  Update right joystick vertical axis (-1.0 for left, 1.0 for right)
            if ax == 3:
                c.update_camera_y(axis)
            #  Update right joystick (-1.0 for up, 1.0 for down)
            if ax == 4:
                c.update_camera_x(axis)
