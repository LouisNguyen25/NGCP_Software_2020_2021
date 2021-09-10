from controller import Robot, Camera, CameraRecognitionObject, Receiver
import math, cv2
import numpy as np

TIME_STEP = 64
MOR = math.pi/100   #this is the minimum allowed radian difference when determing if facing dest
MOD = 0.35          #minimum allowed distance to target to stop
robot = Robot()
ds = []

count = 0

#all the different components of the robot
leftEye = robot.getCamera('leftEye')
leftEye.enable(TIME_STEP)
leftEye.recognitionEnable(TIME_STEP)

rightEye = robot.getCamera('rightEye')
rightEye.enable(TIME_STEP)
rightEye.recognitionEnable(TIME_STEP)

cameras = [leftEye, rightEye]
stereo = cv2.StereoSGBM_create(numDisparities=16, blockSize=10)

distance_threshold = 20
turn_resolution = 2
speed = 3.0

avoidObstacle = 0
RyansFlag = True

gps = robot.getGPS("gps")
gps.enable(TIME_STEP)

receiver = robot.getReceiver("receiver")
receiver.enable(TIME_STEP)
oldDestination = ""

compass = robot.getCompass("compass")
compass.enable(TIME_STEP)

leftSpeed = 3.0
rightSpeed = 3.0
tankTurning = False
destRecieved = False

#assigning wheels to their relative pieces on the bot
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(speed)
avoidObstacleCounter = 0

#turns our bot until within a specific angle to our dest  
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

#main loop
while robot.step(TIME_STEP) != -1:
    cameras[1].saveImage('left.png',90)
    cameras[0].saveImage('right.png',90)
    
    l_mat = cv2.imread('left.png',0)
    r_mat = cv2.imread('right.png',0)
    
    
    disparity = stereo.compute(l_mat,r_mat)
    cv2.imwrite('depth.png',disparity)
    cropped = disparity[16:-8,16:-8]
    down_scaled = cv2.resize(cropped,(10,3))
    
    if max(down_scaled[1]) >= distance_threshold:
       avoidObstacle = turn_resolution
       if np.argmax(down_scaled[1]) <= len(down_scaled[1])/2:
           leftSpeed = -speed
           rightSpeed = speed
       else:
           leftSpeed = speed
           rightSpeed = -speed
    elif avoidObstacle > 0:
        avoidObstacle -= 1
    else:
        print(count)
        count += 1
        leftSpeed = speed
        rightSpeed = speed  
    if True:
        #gets information from the destination sender
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
                rightSPeed = speed
        else:
            leftSpeed = 0
            rightSPeed = 0      
    wheels[0].setVelocity(rightSpeed)
    wheels[1].setVelocity(rightSpeed)
    wheels[2].setVelocity(leftSpeed)
    wheels[3].setVelocity(leftSpeed) 