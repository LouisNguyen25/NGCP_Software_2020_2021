import concurrent.futures
import time, math, requests, sys, keyboard
import RPi.GPIO as GPIO

#PINS = [23, 24, 25]

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.FALLING)
   
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(24, GPIO.FALLING)   

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(25, GPIO.FALLING)

# for pin in PINS :
#    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#    GPIO.add_event_detect(pin, GPIO.FALLING)

""" 
Thread for GCS (Comms)
Thread for other processes (Camera, Waypoint Nav, IMU, & Obj Detect)

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
"""

def gcs_system(btn23Pressed):
   print("Into GCS_System")
   while True:  # making a loop
      try:  # used try so that if user pressed other than the given key error will not be shown
         if btn23Pressed:  # if key 'c' is pressed 
            print('You Pressed the 23 button!')
            break  # finishing the loop
      except:
         print("Exception GCS")
         break  # if user pressed a key other than the given key the loop will break
   print("Exited GCS_System")

def our_stuff1(btn24Pressed):
   print("Into Stuff1")
   while True:  # making a loop
      try:  # used try so that if user pressed other than the given key error will not be shown
         if btn24Pressed:  # if key 'c' is pressed 
            print('You Pressed the 24 button!')
            break  # finishing the loop
      except:
         print("Exception Stuff1")
         break  # if user pressed a key other than the given key the loop will break
   print("Exited Stuff1")

def our_stuff2(btn25Pressed):
   print("Into Stuff2")
   while True:  # making a loop
      try:  # used try so that if user pressed other than the given key error will not be shown
         if btn25Pressed:  # if key 'c' is pressed 
            print('You Pressed the 25 button!')
            break  # finishing the loop
      except:
         print("Exception Stuff2")
         break  # if user pressed a key other than the given key the loop will break
   print("Exited Stuff2")

def gcs_thread(btn23Pressed):
#    t1 = time.perf_counter()
   with concurrent.futures.ThreadPoolExecutor() as executor:
      f1 = executor.submit(gcs_system, btn23Pressed)
   return "Process is done for GCS_Thread"
#    t2 = time.perf_counter()
#    print(f"Threading/Multiprocessing  took {t2 - t1} second(s)")

def everything_else_thread(btn24Pressed, btn25Pressed):
   #t1 = time.perf_counter()
   with concurrent.futures.ThreadPoolExecutor() as executor:
      f1 = executor.submit(our_stuff1, btn24Pressed)
      f2 = executor.submit(our_stuff2, btn25Pressed)
   return "Process is done for everything else"

def main() :
   btn23Pressed = GPIO.event_detected(23)
   btn24Pressed = GPIO.event_detected(24)
   btn25Pressed = GPIO.event_detected(25)

   with concurrent.futures.ProcessPoolExecutor() as executor:
      p1 = executor.submit(gcs_thread, btn23Pressed)
      p2 = executor.submit(everything_else_thread, btn24Pressed, btn25Pressed)

      print(p1.result())
      print(p2.result())


if __name__ == '__main__':
   main()



'''

def counter1() :
   print("Entered Counter1")
   while True:  # making a loop
      try:  # used try so that if user pressed other than the given key error will not be shown
         if GPIO.event_detected(23):  # if key 'c' is pressed 
            print('You Pressed A Button!')
            break  # finishing the loop
      except:
         continue  # if user pressed a key other than the given key the loop will break


def counter2() :
   print("Entered counter2")
   for _ in range(100_000_000) :
      continue
   return 2

def counter3():
   while True:  # making a loop
      try:  # used try so that if user pressed other than the given key error will not be shown
         if keyboard.is_pressed('a'):  # if key 'a' is pressed 
            print('You Pressed A Key!')
            break  # finishing the loopa
      except:
         break  # if user pressed a key other than the given key the loop will break


img_urls = [
    'https://images.unsplash.com/photo-1516117172878-fd2c41f4a759',
    'https://images.unsplash.com/photo-1532009324734-20a7a5813719',
    'https://images.unsplash.com/photo-1524429656589-6633a470097c',
    'https://images.unsplash.com/photo-1530224264768-7ff8c1789d79',
    'https://images.unsplash.com/photo-1564135624576-c5c88640f235',
    'https://images.unsplash.com/photo-1541698444083-023c97d3f4b6',
    'https://images.unsplash.com/photo-1522364723953-452d3431c267',
    'https://images.unsplash.com/photo-1513938709626-033611b8cc03',
    'https://images.unsplash.com/photo-1507143550189-fed454f93097',
    'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e',
    'https://images.unsplash.com/photo-1504198453319-5ce911bafcde',
    'https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99',
    'https://images.unsplash.com/photo-1516972810927-80185027ca84',
    'https://images.unsplash.com/photo-1550439062-609e1531270e',
    'https://images.unsplash.com/photo-1549692520-acc6669e2f0c'
]


def download_image(img_url):    
   img_bytes = requests.get(img_url).content   
   img_name = img_url.split("/")[3]   
   img_name = f"pics/{img_name}.jpg"     
   with open(img_name, 'wb') as img_file:   
        img_file.write(img_bytes)     
        print(f"{img_name} was downloaded...")    

def concurrent_threads():
    counter1()
    counter2()

    return 0
    

def main():
   t1 = time.perf_counter()
   with concurrent.futures.ThreadPoolExecutor() as executor:
      
      f1 = executor.submit(concurrent_threads)
      executor.map(download_image, img_urls)
      f2 = executor.submit(counter3)


      print(f1.result())
      print(f2.result())
      # print(f3.result())

   t2 = time.perf_counter()
   print(f"Threading/Multiprocessing took {t2 - t1} second(s)")

   # t3 = time.perf_counter()

   # counter1()
   # counter2()
   # # map(download_image, img_urls)
   
   # t4 = time.perf_counter()
   # print(f"Sequential Processes took {t4 - t3} second(s)")

if __name__ == '__main__':
   main()

'''