# 448 0 degree -> Multiply by 4 in setTarget
# 2544 180 degree
import maestro
import time
servo = maestro.Controller(ttyStr='/dev/ttyACM0')

arms = 0.0
claws = 0.0
max_speed = 10
conversionValue = 2

servoMinRange = 448
servoMaxRange = 2554

arms = float(input("A: ")) # man_con.arm
claws = float(input("C: ")) # man_con.claw

def setServo(servoNum, minimum, maximum) :
    servo.setRange(servoNum,minimum,maximum)
    print(f"The target =  {servo.getPosition(servoNum)}.")
    print(f"The target is moving = {servo.isMoving(servoNum)}")
    servo.setAccel(servoNum,0)
    servo.setSpeed(servoNum,15)

def clamp(value, minimum, maximum):
    if(value < minimum):
        return minimum
    if(value > maximum):
        return maximum
    return value

def MotorMove(servoNumber, target):
    print("Clamped Value: ", clamp(target, servoMinRange, servoMaxRange))
    servo.setTarget(servoNumber, clamp(target, servoMinRange, servoMaxRange) * conversionValue)

setServo(0,servoMinRange*conversionValue,servoMaxRange*conversionValue)
setServo(1,servoMinRange*conversionValue,servoMaxRange*conversionValue)

while True :
    print()
    time.sleep(.5)
    
    targetArms = (int)(servo.getPosition(0)/conversionValue)
    targetClaw = (int)(servo.getPosition(1)/conversionValue)

    stepSize = 300

    if arms < 0:
        targetArms -= (int)(stepSize * abs(arms))
    elif arms > 0:
        targetArms += (int)(stepSize * abs(arms))

    if claws < 0:
        targetClaw -= (int)(stepSize * abs(claws))
    elif claws > 0:
        targetClaw += (int)(stepSize * abs(claws))
        
    
    MotorMove(0, targetArms)
    MotorMove(1, targetClaw)
servo.close

#(◕‿◕)
# ================================================================

# ʕ·(エ)· ʔ
# ^^^ Brendon's fav bear so far

# 
#       _o_|_o_|_x_
#       _x_|_o_|_o_
#        o | x | x  

# Hangman anyone?    
# 
#    __
#   |  \ 
#   |                 _ _ _ _   _ _ _ _ _ _ _   _ _   _ _ _ _ _ _ _! 
#   |   
#   |                   Guessed: a
#  _|_

# i had to hide the evidence
# life is tuff
# ʕ ·ᴥ·ʔ
# ʕ·㉨· ʔ

#( ͡° ͜ʖ ͡°)
#( ◉◞౪◟◉)
# ʕ灬￫ᴥ￩灬ʔ

#⎝ ⏠⏝⏠⎠
# ( ͡Ⓘ ͜ʖ ͡Ⓘ) (◕‿◕)
#/╲/\╭( ͡°͡° ͜ʖ ͡°͡°)╮/\╱\

#  ▬▬▬.◙.▬▬▬
#  ═▂▄▄▓▄▄▂
# ◢◤ █▀▀████▄▄▄▄◢◤
# █▄▂█ █▄███▀▀▀▀▀▀▀╬
# ◥█████◤
# ══╩══╩═
#  ╬═╬
#  ╬═╬
#  ╬═╬
#  ╬═╬
#  ╬═╬
#  ╬═╬ ☻/ -- to hell with the ERU, I got us a helicopter!
#  ╬═╬/▌
#  ╬═╬/

# (༎ຶꈊ༎ຶ╬ ) ⊂(•̀﹏•́⊂ )∘˚˳°
# ( ͡°͜ ͡°)
# ༼   ºل͟º ༼   ºل͟º ༼   ºل͟º  ༽ ºل͟º  ༽ ºل͟º  ༽G