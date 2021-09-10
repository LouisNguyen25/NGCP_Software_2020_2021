import FaBo9Axis_MPU9250
import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(23, GPIO.FALLING)

class mpuClass_2_5 :
    NUMBER_OF_ITERATIONS = 10
    SIG_FIGS = 4
    UPSIDE_DOWN = -0.2
    CHUTE_CHECK = 0.5
    ACCEL_THRESH = 0.5
    GYRO_THRESH  = 5.0
    MAG_THRESH = 5.0
    LAND_COUNT = 10

    GFS_250 = 0x00
    GFS_500 = 0x01
    GFS_1000 = 0x02
    GFS_2000 = 0x03

    AFS_2G = 0x00
    AFS_4G = 0x01
    AFS_8G = 0x02
    AFS_16G = 0x03
    
    def __init__(self) :

        self.isUpsideDown = False
        self.isChuteDeployed = False
        self.isLanded = False

        self.ax_prev, self.ay_prev, self.az_prev = 0, 0, 1
        self.mx_prev, self.my_prev, self.mz_prev = 0, 0, 0
        self.gox, self.goy, self.goz = 0, 0, 0

        self.mpu = FaBo9Axis_MPU9250.MPU9250()
    
# Only when all measurements are stable within stated thresholds will this return 1 and add to
# landed sequence - for now if landCount reaches 10 we will assume we have landed
# as of Feb 05 working with accel_thresh: 0.5, gyro_thresh:5.0, mag_thresh: 5.0
    def checkLanded(self, curAccel, curGyro, curMag):
        print("Got into check landed")
        if abs(curAccel['x'] - self.ax_prev) > mpuClass_2_5.ACCEL_THRESH:
            return 0
        elif abs(curAccel['y'] - self.ay_prev) >  mpuClass_2_5.ACCEL_THRESH:
            return 0
        elif abs(curAccel['z'] - self.az_prev) >  mpuClass_2_5.ACCEL_THRESH:
            return 0
            
        elif abs(curGyro['x'] - self.gox) >  mpuClass_2_5.GYRO_THRESH:
            return 0
        elif abs(curGyro['y'] - self.goy) >  mpuClass_2_5.GYRO_THRESH:
            return 0
        elif abs(curGyro['z'] - self.goz) >  mpuClass_2_5.GYRO_THRESH:
            return 0

        elif abs(curMag['x'] - self.mx_prev) >  mpuClass_2_5.MAG_THRESH:
            return 0
        elif abs(curMag['y'] - self.my_prev) >  mpuClass_2_5.MAG_THRESH:
            return 0
        elif abs(curMag['z'] - self.mz_prev) >  mpuClass_2_5.MAG_THRESH:
            return 0

        else:
            return 1
            
    def calibrate(self, device):
        aSum = [0, 0, 0]
        gSum = [0, 0, 0]

        for _ in range(mpuClass_2_5.NUMBER_OF_ITERATIONS):
            aSum[0] += device.readAccel()["x"]
            aSum[1] += device.readAccel()["y"]
            aSum[2] += device.readAccel()["z"]

            gSum[0] += device.readGyro()["x"]
            gSum[1] += device.readGyro()["y"]
            gSum[2] += device.readGyro()["z"]

        aox = aSum[0] / mpuClass_2_5.NUMBER_OF_ITERATIONS
        aoy = aSum[1] / mpuClass_2_5.NUMBER_OF_ITERATIONS
        aoz = aSum[2] / mpuClass_2_5.NUMBER_OF_ITERATIONS - 1.0

        gox = gSum[0] / mpuClass_2_5.NUMBER_OF_ITERATIONS
        goy = gSum[1] / mpuClass_2_5.NUMBER_OF_ITERATIONS
        goz = gSum[2] / mpuClass_2_5.NUMBER_OF_ITERATIONS

        return aox, aoy, aoz, gox, goy, goz

    def getOrientation(self):

        mag = self.mpu.readMagnet()
        
        return mag


    def chuteDeployAndLandedCheck(self):
        print("Got into method")
        try:

            landCount, prevLandCount = 0, 0
            print("Before calibrate")
            aox, aoy, aoz, gox, goy, goz = self.calibrate(self.mpu)
            print("Got into Try chute deploy")
            while not self.isLanded:

                accel = self.mpu.readAccel()
                
                # print("az = ", round(accel['z'] - aoz, self.SIG_FIGS))
                
                gyro = self.mpu.readGyro()
                print("gx = ", round(gyro['x'] - gox, mpuClass_2_5.SIG_FIGS), "deg/sec")
                print("gy = ", round(gyro['y'] - goy, mpuClass_2_5.SIG_FIGS))
                print("gz = ", round(gyro['z'] - goz, mpuClass_2_5.SIG_FIGS))

                mag = self.mpu.readMagnet()

                if GPIO.event_detected(23):
                    aox, aoy, aoz, gox, goy, goz = self.calibrate(self.mpu)
                    print("RECALIBRATED!!!")

                if accel['z'] < mpuClass_2_5.UPSIDE_DOWN:
                    self.isUpsideDown = True
                    print("Upside Down!!")

                else:
                    self.isUpsideDown = False


                if accel['z'] - self.az_prev > mpuClass_2_5.CHUTE_CHECK:
                    self.isChuteDeployed = True
                    print("==========!!!PARACHUTE DEPLOYED!!!==========")

                else:
                    self.isChuteDeployed = False

                landCount += self.checkLanded(accel, gyro, mag)
                print("land count: ", landCount)

                """ Reassign *_prev values """

                self.ax_prev = accel['x']
                self.ay_prev = accel['y']
                self.az_prev = accel['z']

                self.mx_prev = mag['x']
                self.my_prev = mag['y']
                self.mz_prev = mag['z']

                if landCount >= self.LAND_COUNT:
                    self.isLanded = True
                    print("Landed!")

                if prevLandCount == landCount:
                    landCount = 0
                    self.isLanded = False

                prevLandCount = landCount

                print(" ")
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("===========Keyboard Interrupt for Class============")
            sys.exit()


        return print("Exited chuteDeployedAndLandedCheck()")