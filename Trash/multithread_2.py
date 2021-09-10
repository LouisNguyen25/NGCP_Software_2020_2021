import threading, time, keyboard
import concurrent.futures

'''
===============================================================================
processOne():
with concurrent.futures.ThreadPoolExecutor() as executor:
   threadOne - GCS COMM
   

processTwo():
with concurrent.futures.ThreadPoolExecutor() as executor:
   threadTwo - CAMERA
   threadThree - WAYPOINT NAV
   
main():
with concurrent.futures.ProcessPoolExecutor() as executor:
   processOne - goes to one core
   processTwo - goes to other core
===============================================================================
'''

def gcs_system():
    print("Into GCS_System")
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
           if keyboard.is_pressed('a'):  # if key 'c' is pressed 
               print('You Pressed a!')
               break  # finishing the loop
        except:
            # print("Exception")
            break  # if user pressed a key other than the given key the loop will break
    print("Exited GCS_System")

def our_stuff1():
    print("Into Stuff1")
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
           if keyboard.is_pressed('b'):  # if key 'c' is pressed 
               print('You Pressed b!')
               break  # finishing the loop
        except:
            break  # if user pressed a key other than the given key the loop will break
    print("Exited Stuff1")

def our_stuff2():
    print("Into Stuff2")
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
           if keyboard.is_pressed('c'):  # if key 'c' is pressed 
               print('You Pressed c!')
               break  # finishing the loop
        except:
            break  # if user pressed a key other than the given key the loop will break
    print("Exited Stuff2")

def gcs_thread():
#    t1 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(gcs_system)
    return "Process is done for GCS_Thread"
#    t2 = time.perf_counter()
#    print(f"Threading/Multiprocessing  took {t2 - t1} second(s)")

def everything_else_thread():
   #t1 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(our_stuff1)
        f2 = executor.submit(our_stuff2)
    return "Process is done for everything else"

def main() :
    with concurrent.futures.ProcessPoolExecutor() as executor:
        p1 = executor.submit(gcs_thread)
        p2 = executor.submit(everything_else_thread)

        print(p1.result())
        print(p2.result())


if __name__ == '__main__':
   main()