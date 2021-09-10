"""
IMU Integration for the MPU9250 - 01/09/2021 (flags and threads)

"""
import FaBo9Axis_MPU9250
import RPi.GPIO as GPIO
import time, sys

NUMBER_OF_ITERATIONS = 10
SIG_FIGS = 4
UPSIDE_DOWN = -0.2
bUPSIDE_DOWN = False
CHUTE_CHECK = 0.5
bCHUTE_CHECK = False
ACCEL_THRESH = 0.5
GYRO_THRESH  = 0.2
MAG_THRESH   = 5.0
LAND_COUNT = 10
bLANDED = False

GFS_250 = 0x00
GFS_500 = 0x01
GFS_1000 = 0x02
GFS_2000 = 0x03

AFS_2G = 0x00
AFS_4G = 0x01
AFS_8G = 0x02
AFS_16G = 0x03

# mpu.configMPU9250(GFS_250, AFS_2G)


# Sets up an interrupt in order to calibrate by pressing a button
GPIO.setmode(GPIO.BCM)
# GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.FALLING)

mpu = FaBo9Axis_MPU9250.MPU9250()

def main():

    try:

        ax_prev, ay_prev, az_prev = 0, 0, 1
        mx_prev, my_prev, mz_prev = 0, 0, 0
        landCount, prevLandCount = 0, 0

        aox, aoy, aoz, gox, goy, goz = calibrate(mpu)

        while ("""button 24 is NOT pressed"""):

            accel = mpu.readAccel()
            # print("ax = ", round(accel['x'] - aox, SIG_FIGS), "G")
            # print("ay = ", round(accel['y'] - aoy, SIG_FIGS))
            print("az = ", round(accel['z'] - aoz, SIG_FIGS))

            gyro = mpu.readGyro()
            # print("gx = ", round(gyro['x'] - gox, SIG_FIGS), "deg/sec")
            # print("gy = ", round(gyro['y'] - goy, SIG_FIGS))
            # print("gz = ", round(gyro['z'] - goz, SIG_FIGS))

            mag = mpu.readMagnet()
            # print("mx = ", mag['x'])
            # print("my = ", mag['y'])
            # print("mz = ", mag['z'])

            # temp = mpu.readTemp()
            # print("temp = ", temp, " deg C\n")

            if GPIO.event_detected(23):
                aox, aoy, aoz, gox, goy, goz = calibrate(mpu)
                print("RECALIBRATED!!!")

            # Parachute / Upside Down
            if accel['z'] < UPSIDE_DOWN:
                bUPSIDE_DOWN = True
                print("Upside Down!!")

            else:
                bUPSIDE_DOWN = False


            if accel['z'] - az_prev > CHUTE_CHECK:
                bCHUTE_CHECK = True
                print("==========!!!PARACHUTE DEPLOYED!!!==========")

            else:
                bCHUTE_CHECK = False

            landCount += checkLanded(accel, gyro, mag)
            # print("land count: ", landCount)

            """ Reassign *_prev values """
            ax_prev = accel['x']
            ay_prev = accel['y']
            az_prev = accel['z']

            mx_prev = mag['x']
            my_prev = mag['y']
            mz_prev = mag['z']

            if landCount >= LAND_COUNT:
                bLANDED = True
                print("Landed!")

            if prevLandCount == landCount:
                landCount = 0
                bLANDED = False

            prevLandCount = landCount

            print(" ")
            time.sleep(0.25)

    except KeyboardInterrupt:
        sys.exit()

def calibrate(device):
    aSum = [0, 0, 0]
    gSum = [0, 0, 0]

    for _ in range(NUMBER_OF_ITERATIONS):
        aSum[0] += device.readAccel()["x"]
        aSum[1] += device.readAccel()["y"]
        aSum[2] += device.readAccel()["z"]

        gSum[0] += device.readGyro()["x"]
        gSum[1] += device.readGyro()["y"]
        gSum[2] += device.readGyro()["z"]

    aox = aSum[0] / NUMBER_OF_ITERATIONS
    aoy = aSum[1] / NUMBER_OF_ITERATIONS
    aoz = aSum[2] / NUMBER_OF_ITERATIONS - 1.0

    gox = gSum[0] / NUMBER_OF_ITERATIONS
    goy = gSum[1] / NUMBER_OF_ITERATIONS
    goz = gSum[2] / NUMBER_OF_ITERATIONS

    return aox, aoy, aoz, gox, goy, goz

# Only when all measurements are stable within a stated threshold will this return 1 and add to
# landed sequence - for now if landCount reaches 10 we will assume we have landed
def checkLanded(curAccel, curGyro, curMag):

    if abs(curAccel['x'] - ax_prev) > ACCEL_THRESH:
        return 0
    elif abs(curAccel['y'] - ay_prev) > ACCEL_THRESH:
        return 0
    elif abs(curAccel['z'] - az_prev) > ACCEL_THRESH:
        return 0

    elif abs(curGyro['x'] - gox) > GYRO_THRESH:
        return 0
    elif abs(curGyro['y'] - goy) > GYRO_THRESH:
        return 0
    elif abs(curGyro['z'] - goz) > GYRO_THRESH:
        return 0

    elif abs(curMag['x'] - mx_prev) > MAG_THRESH:
        return 0
    elif abs(curMag['y'] - my_prev) > MAG_THRESH:
        return 0
    elif abs(curMag['z'] - mz_prev) > MAG_THRESH:
        return 0

    else:
        return 1

main()
