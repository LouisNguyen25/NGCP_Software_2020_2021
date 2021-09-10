import serial # Allows access to serial ports
import time # Allows access to time and operations
import string # Allows access to string operations
import pynmea2 # Python library for the NMEA 0183 protocol
import math
from Camera import camera2
from IMU import mpu9250_i2c
from mpu9250_i2c import *
from magnetic_field_calculator import MagneticFieldCalculator
from datetime import datetime

MOD = 0.35 # minimum allowed distance to target to stop
MOR = math.pi/100   #this is the minimum allowed radian difference when determing if facing dest
hiker_location = (37, 117) # destination (lat, long)

def get_current_location(old_location=(0,0)):
    '''
    Gets current location of bot in (lat, long) coordinates
    '''
    try:
        port="/dev/ttyAMA0"
        ser=serial.Serial(port,baudrate=9600,timeout=0.5) # Configures serial port, baudrate, and period
        gps_data_0=ser.readline() # Reads data from port
        gps_data_1=gps_data_0.decode('UTF-8',errors='strict') # Decodes raw byte data type to string data type

        if gps_data_1[0:6]=="$GNRMC": # If the first 6 bits are $GNRMC (GPS signal)
            new_signal=pynmea2.parse(gps_data_1) # Converts raw data using pynmea2 protocol
            lat=new_signal.latitude # Defines lat as latitude data of new_signal
            lng=new_signal.longitude # Defines lng as longitude data of new signal
            latitude=round(lat,5) # Rounds lat to 5 significant figures
            longitude=round(lng,5) # Rounds lng to 5 significant figures
            return (latitude, longitude)
    except UnicodeDecodeError:
        #print((latitude, longitude))
        return old_location

def closeEnough():
    '''
    Function to check if current bot location is relatively close to hiker location
    '''
    curLocation = get_current_location()
    
    xLen = float(hiker_location[0]) - curLocation[0]
    zLen = float(hiker_location[1]) - curLocation[2]
    
    distance = math.sqrt(xLen * xLen + zLen * zLen)
    return False if distance > MOD else True

def findBearing(latStart, longStart, latEnd, longEnd):
    '''
    Returns the angle and distance between bot and hiker location
    '''
    dLat = (latEnd - latStart) * math.pi / 180.0
    dLon = (longEnd - longStart) * math.pi / 180.0
    latStart = latStart * math.pi / 180.0
    latEnd = latEnd * math.pi / 180.0
    y = math.sin(dLon) * math.cos(latEnd)
    x = math.cos(latStart) * math.sin(latEnd) - math.sin(latStart) * math.cos(latEnd) * math.cos(dLon)
    bearing = math.atan2(y, x)
    return bearing

def getDeclination(lat, long):
    '''
    Returns the offset between magnetic north and true north
    '''
    calculator = MagneticFieldCalculator()
    result = calculator.calculate(
        latitude=lat,
        longitude=long,
        date=datetime.today().strftime('%Y-%m-%d')
    )

    field_value = result['field-value']
    return field_value['declination']

def correctHeading():
    '''
    Ensures the bot is moving at the correct heading toward the hiker location
    '''
    #curLocation = get_current_location()
    while(True):
        bearing = findBearing(hiker_location[0], hiker_location[1], curLocation[0], curLocation[1]) # relative to true north
        declination = getDeclination(curLocation[0], curLocation[1])

        #gets current direction
        mx, my, mz = AK8963_conv()
        curDirection = math.atan2(my,mx) # heading of bot relative to magnetic north
        curDirection *= 180/math.pi # converting to degrees
        curDirection -= (declination['value'] * math.pi/180) # adjust current direction to be relative to true north
        if curDirection < 0:
                curDirection += 360

        #makes everything on a 0-2pi scale
        if bearing < 0:
             bearing += math.pi * 2
        if curDirection < 0:
             curDirection += math.pi * 2

    while difference <= MOR:
        '''
        Adjust heading until bot is facing the correct heading
        '''
        curLocation = get_current_location()
        bearing = findBearing(curLocation[0], curLocation[1], hiker_location[0], hiker_location[1])
        declination = getDeclination(curLocation[0], curLocation[1])

        # gets current direction
        mx, my, mz = AK8963_conv()

        # account for imu being upside and reverse
        if my >= 0:
            my -= math.pi
        else:
            my += math.pi

        curDirection = math.atan2(my,mx)
        curDirection -= (declination['value'] * math.pi/180)
        # curDirection *= math.pi/180 # convert to radians
        if curDirection < 0:
            curDirection += 360

        # makes everything on a 0-2pi scale
        if bearing < 0:
            bearing += math.pi * 2
        if curDirection < 0:
            curDirection += math.pi * 2
    
        difference = abs(curDirection - bearing)
        arc = (curDirection - bearing) % (math.pi * 2)
        turnRight = False if arc < math.pi else True    
        if turnRight:
            # set motors to turn bot right
            pass
        else:
            # set motors to turn bot left
            pass
    # set motors to go straight again
    return

while True:
    bot_location = get_current_location() # Get bots current (lat, long)

    if(camera2.cameraFeed() != 0): # Check if obstacle is obstructing bots path
        print("avoiding obstacle")
        # obstacle avoidance function
        pass
    # Add timer to go straight for 2sec after object avoidance
    elif(camera2.cameraFeed() == 0):
        correctHeading()
        print("going to dest")
        # continue navigating to destination
        pass

    # if(closeEnough()):
    #     print("close to hiker")
    #     # stop nagivation, communicate w gcs, power off motors
    #     break