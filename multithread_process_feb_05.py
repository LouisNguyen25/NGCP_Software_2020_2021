"""
For general testing and whatnot
"""
import multiprocessing
import concurrent.futures
import RPi.GPIO as GPIO
from MPU import mpuClass_2_5 as mpuClass

# from .. import MPU
# from MPU import mpuClass_2_5 as mpuClass

GPIO.setmode(GPIO.BCM)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(24, GPIO.FALLING)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(25, GPIO.FALLING)

# TODO: Implement callbacks for multithreading/xbee

# TODO: Find out how to acquire/lock data

def press24():

    #If btn 24 is pressed - return coms
    #if btn 25 is pressed - return waypoint
    #COMS
    #WAYPOINT

    """ Call mpu9250.main() """
    """while True:
            run that function
            gpio event makes it false """

    print("Entered press24")
    # while True:
    
    mpuObj = mpuClass.mpuClass_2_5()
    orientation = mpuObj.mpu.readMagnet()
    print("Orientation: ", orientation)

    
    mpuObj.chuteDeployAndLandedCheck()
            
    print("Returned from class method")
    if GPIO.event_detected(24):
        print("Pressed button 24!")
            #break

def press25():
    print("Entered press25")
    while True:
        if GPIO.event_detected(25):
            print("Pressed button 25!")
            break

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("concurrent is working")
        f2 = executor.submit(press24)
        f3 = executor.submit(press25)

    print("All threads have been run.")

if __name__ == '__main__':
   main()
