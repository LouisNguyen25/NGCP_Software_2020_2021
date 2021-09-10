"""four_wheeled controller."""
from controller import Robot, Camera, CameraRecognitionObject, Receiver
import math, cv2, time, calendar
import numpy as np


TIME_STEP = 64
MOR = math.pi/100   #this is the minimum allowed radian difference when determing if facing dest
MOD = 0.35          #minimum allowed distance to target to stop
robot = Robot()
ds = []
tankTurning = False
destRecieved = False

wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)


gps = robot.getGPS("gps")
gps.enable(TIME_STEP)

receiver = robot.getReceiver("receiver")
receiver.enable(TIME_STEP)
oldDestination = ""

compass = robot.getCompass("compass")
compass.enable(TIME_STEP)

cameras = [robot.getCamera('cameraL'),robot.getCamera('cameraR')]
cameras[0].enable(TIME_STEP)
cameras[1].enable(TIME_STEP)
stereo = cv2.StereoSGBM_create(numDisparities=16, blockSize=10)

def tankTurn(dest):
    curLocation = gps.getValues()

    #makes the dest turn into a list with x at index 1 and z at index 2
    dest = str(dest,'utf-8')
    dest = dest.split(' ')
    xLen = float(dest[0]) - curLocation[0]
    zLen = float(dest[1]) - curLocation[2]
    
    heading = math.atan(zLen/xLen)

    #gets current direction
    compassRotations = compass.getValues()
    curDirection = math.atan(compassRotations[0]/compassRotations[2])

    if xLen < 0:
        heading = heading + math.pi
    if compassRotations[2] < 0:
        curDirection = curDirection + math.pi
        pass

    #makes everything on a 0-2pi scale
    if heading < 0:
        heading += math.pi * 2
    if curDirection < 0:
        curDirection += math.pi * 2

    difference = abs(curDirection - heading)

    #keeps turning until in the specific heading
    if difference <= MOR:
        return [False, speed, speed]
        
    #determines what way we turn
    arc = (curDirection - heading) % (math.pi * 2)
    turnRight = False if arc < math.pi else True    
    
    if turnRight:
        leftSpeed = -speed
        rightSpeed = speed
    else:
        leftSpeed = speed
        rightSpeed = -speed
    return [True, leftSpeed, rightSpeed]
    
def closeEnough(dest):
    dest = str(dest,'utf-8')
    dest = dest.split(' ')

    if(dest[0] == ''):
        return False

    curLocation = gps.getValues()
    
    xLen = float(dest[0]) - curLocation[0]
    zLen = float(dest[1]) - curLocation[2]
    
    distance = math.sqrt(xLen * xLen + zLen * zLen)
    return False if distance > MOD else True

distance_threshold = 65
turn_resolution = 2
speed = 2
avoidObstacle = 0
leftSpeed = 1.0
rightSpeed = 1.0
avoided = False

while robot.step(TIME_STEP) != -1:
    
    cameras[0].saveImage('left.png',90)
    cameras[1].saveImage('right.png',90)
    
    l_mat = cv2.imread('left.png',0)
    r_mat = cv2.imread('right.png',0)
    
    
    disparity = stereo.compute(l_mat,r_mat)
    cropped = disparity[16:-8,16:-8]
    down_scaled = cv2.resize(cropped,(10,3))
    cv2.imwrite('depth.png',disparity)
    
    #if there is an object close enough to avoid
    if max(down_scaled[1]) >= distance_threshold:
        avoidObstacle = turn_resolution
        #if object is to our left
        if np.argmax(down_scaled[1]) <= len(down_scaled[1])/2:
            leftSpeed = speed
            rightSpeed = -speed
        #if object is to our right
        else:
            leftSpeed = -speed
            rightSpeed = speed
    #if we are still avoiding an obstacle
    elif avoidObstacle > 0:
        avoidObstacle -= 1
        x_time = (calendar.timegm(time.gmtime()))
        avoided = True
    #if avoided reset the values to normal
    elif avoided:
        if(calendar.timegm(time.gmtime()) - x_time > 2):
            avoided = False
            tankTurning = True
        else:
            leftSpeed = speed
            rightSpeed = speed
    #otherwise ensure we are going towards the right waypoint
    else:
        if receiver.getQueueLength() > 0:
            destination = receiver.getData()
            destRecieved = True
            if destination != oldDestination:
                oldDestination = destination
                receiver.nextPacket()
                tankTurning = True
        
        #need to check if we are within a certain distance
        atTarget = False
        if destRecieved:
            atTarget = closeEnough(oldDestination)
        
        if not atTarget:
            if tankTurning:
                results = tankTurn(oldDestination)
                tankTurning = results[0]
                leftSpeed = results[2]
                rightSpeed = results[1]
            else:
                leftSpeed = speed
                rightSpeed = speed
        else:
            leftSpeed = 0
            rightSpeed = 0
    print(tankTurning)
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(rightSpeed)