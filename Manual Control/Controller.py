import pygame


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
            print("Updated camera x to: ", self.x_cam)  # FOR DEBUGGING
        else:
            self.x_cam = 0

    def update_camera_y(self, y):
        if joystick_moved(y):
            self.y_cam = round(y, 2)
            print("Updated camera y to: ", self.y_cam)  # FOR DEBUGGING
        else:
            self.y_cam = 0

    def get_x_pos(self) :
        return self.x_pos
    def get_y_pos(self) :
        return self.y_pos

pygame.init()

# Initialize the joysticks
pygame.joystick.init()

# Init current input object
c = CurrentInput()

# Main loop
while True:
    # Need to process events for it to work
    for event in pygame.event.get():
        None

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()

        # Usually axis run in pairs, up/down for one, and left/right for the other.
        axes = joystick.get_numaxes()

        continuousAxes = []

        for i in range(axes):
            axis = joystick.get_axis(i)

            #  Write to dataexport.txt
            continuousAxes.append(axis)
            file_object = open("dataexport.txt", "a+")
            file_object.write("{}\n".format(continuousAxes[0]))

            #  Update left joystick horizontal axis (-1.0 for left, 1.0 for right)
            if i == 0:
                c.update_movement_x(axis)
            #  Update left joystick vertical axis (-1.0 for up, 1.0 for down)
            if i == 1:
                c.update_movement_y(axis)

            #  Update right joystick vertical axis (-1.0 for left, 1.0 for right)
            if i == 3:
                c.update_camera_y(axis)
            #  Update right joystick (-1.0 for up, 1.0 for down)
            if i == 4:
                c.update_camera_x(axis)
