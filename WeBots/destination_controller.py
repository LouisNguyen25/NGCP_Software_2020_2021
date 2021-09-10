"""destination_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Emitter
import struct

TIME_STEP = 64
robot = Robot()

gps = robot.getGPS("gps")
gps.enable(TIME_STEP)

emitter = robot.getEmitter("emitter")

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

oldLocation = []

def passLocation(message):  
    location = str(message[0]) + " " + str(message[2])
    msg = bytes(location, 'utf-8')
    emitter.send(msg)    
    return

while robot.step(TIME_STEP) != -1:
    newLocation = gps.getValues()
    if newLocation == oldLocation:
        x = 1
    else:
        passLocation(newLocation)
        oldLocation = newLocation



# i love donald <3 Ryan 
#;)
''' Donald and Ryan, sitting in a tree...
    K-I-S-S-I-N-G '''