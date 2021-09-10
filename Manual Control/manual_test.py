"""
Manual Control workspace - 02/12/2021
"""

#--------------- THIS WORKS ---------------------
import tty, sys, termios

fd = termios.tcgetattr(sys.stdin.fileno())
#TODO: Try these defintions out next time ----> termios.tcsetattr(fd, termios.TCSADRAIN, old)
#fd = sys.stdin.fileno()
#old = tty.tcgetattr(fd)
tty.setcbreak(sys.stdin)

def main():

    try:
        tty.setcbreak(sys.stdin.fileno())
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        ch = sys.stdin.read(1)
        return ord(ch) if ch else None

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, fd)

if __name__ == '__main__':
    main()

# ------------------ THIS WORKS --------------------
# x = 0
# while 1:
#     try:
#         x=sys.stdin.read(1)[0]
#         print(x)
#         if x == "r":
#             print("You pressed r")
#             #   break
#     except KeyboardInterrupt: 
#         print("Exiting...")
#         sys.exit()
# termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)


        
#TODO: Declare Motors
#      Figure out how get keyboard/controller working with Pi
#      When possible, test movements with motor control
#      Problem right now is keyboard inputs aren't working properly - keyboard isn't importing
#      figure it out 


#¯\_(ツ)_/¯
# while True:
#     try :
#         if keyboard.is_pressed('w'):  # Move Forward
#             #Do Stuff
#         if keyboard.is_pressed('a'):  # Move Left 
#             #Do Stuff
#         if keyboard.is_pressed('s'):  # Move Backwards
#             #Do Stuff
#         if keyboard.is_pressed('d'):  # Move Right
#             #Do Stuff
#         if keyboard.is_pressed('UP ARROW'):  # Open Arm (USE ASCII)
#             #Do Stuff
#         if keyboard.is_pressed('DOWN ARROW'):  # Close Arm (USE ASCII)
#             #Do Stuff
#         if keyboard.is_pressed('RIGHT ARROW'):  # Open Arm (USE ASCII)
#             #Do Stuff
#         if keyboard.is_pressed('LEFT ARROW'):  # Open Arm (USE ASCII)
#             #Do Stuff Who put this lol


#     except:
#         print("Exception")
#         break  # if user 
