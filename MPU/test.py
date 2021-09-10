"""
For general testing and whatnot
"""
import multiprocessing
import concurrent.futures
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.FALLING)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(24, GPIO.FALLING)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(25, GPIO.FALLING)

def press23():
    print("Entered press23")
    while True:
        if GPIO.event_detected(23):
            print("Pressed button 23!")
            break

def press24():

    #If btn 24 is pressed - return coms
    #if btn 25 is pressed - return waypoint
    #COMS
    #WAYPOINT


    print("Entered press24")
    while True:
        if GPIO.event_detected(24):
            print("Pressed button 24!")
            break

def press25():
    print("Entered press25")
    while True:
        if GPIO.event_detected(25):
            print("Pressed button 25!")
            break

# Threading by itself works with GPIO        
def singleThread():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(press23)

def multiThread() :
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f2 = executor.submit(press24)
        f3 = executor.submit(press25)

# Error is in ProcessPoolExecutor
def main():
    # singleThread()
    # multiThread()
    
    # p1 = multiprocessing.Process(target=press23)
    # p2 = multiprocessing.Process(target=multiThread)

    # p1.start()
    # p2.start()

    # p1.join()
    # p2.join()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("concurrent is working")
        p1 = executor.submit(singleThread)
        p2 = executor.submit(multiThread)

if __name__ == '__main__':
   main()