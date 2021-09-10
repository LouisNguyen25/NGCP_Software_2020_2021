import motor_control

RGHT = 0
LEFT = 1
BOTH = 2
FWD  = 0
REV  = 1

motor = MotorClass()

# Manual control tank turning for GCS

try:
    while True:
        vertical = float(input("V: "))
        horizontal = float(input("H: "))
        speed = int(input("Spd: "))        

        # percentage(motor, direction, percent)
        motor.percentage(RGHT, FWD, speed*max(-1, min(horizontal+vertical, 1)))
        motor.percentage(LEFT, FWD, speed*max(-1, min(-horizontal+vertical, 1)))
                
except KeyboardInterrupt():
    print("Exiting...")
finally:
    motor.destroy()