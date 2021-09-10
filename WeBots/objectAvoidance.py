from controller import Robot, Camera, Motor

robot = Robot()
timestep = int(robot.getBasicTimeStep())

cam = robot.getCamera("camera")

# initialize motors
wheels = []
wheelsNames = ["frontLeft", "frontRight", "backLeft", "backRight"]

MAX_DIST = 100      # [cm]
MIN_DIST = 25

# Main Loop:
while robot.step(timestep) != -1:
    distance = cam.getNear()

    if distance > MAX_DIST:
        # move forward

    elif distance < MAX_DIST and distance > MIN_DIST:
        # turn

    else:
        # default (move backward)

    image = cam.getImage()