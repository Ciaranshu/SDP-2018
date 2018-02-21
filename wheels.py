import ev3dev.ev3 as ev3
import sys
import helpers as hp
from time import sleep,time

""" USAGE OF WHEELS:
python3 wheels 0 distance -> go back distance
python3 wheels 1 distance -> go forward distance
python3 wheels 2 angle -> rotate Clockwise angle degrees
python3 wheels 3 angle -> rotate anticlockwise angle degrees
"""
def resetPositions():
    rWheel.position = 0
    lWheel.position = 0

def goBackwards(distance, speed=500):
    hp.setMotors([rWheel, lWheel],[distance + rWheel.position, lWheel.position - distance], speed)

def goForwards(distance, speed=500):
    hp.setMotors([rWheel, lWheel],[-distance + rWheel.position, lWheel.position + distance], speed)

def resetGyro():
    gyroSensor.mode = 'GYRO-RATE'
    gyroSensor.mode = 'GYRO-ANG'

def rotateClockwise(angle, speed=-500):
    resetGyro()
    while(gyroSensor.angle <= angle+1):
        print(gyroSensor.angle)
        rWheel.run_forever(speed_sp = speed)
        lWheel.run_forever(speed_sp = speed)
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")

def rotateAntiClockwise(angle, speed=-500):
    resetGyro()
    angle = - abs(angle)
    while(gyroSensor.angle >= angle-1):
        print(gyroSensor.angle)
        rWheel.run_forever(speed_sp = speed)
        lWheel.run_forever(speed_sp = speed)
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")

def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


rWheel = ev3.MediumMotor('outA')
lWheel = ev3.MediumMotor('outB')
gyroSensor = ev3.GyroSensor(ev3.INPUT_1)


if representsInt(sys.argv[1]) and representsInt(sys.argv[2]):
    typeOfMovement = int (sys.argv[1])
    if typeOfMovement == 0:
        distance = int (sys.argv[2])
        goBackwards(distance)
    elif typeOfMovement == 1:
        distance = int (sys.argv[2])
        goForwards(distance)
    elif typeOfMovement == 2:
        angle = int (sys.argv[2])
        rotateClockwise(angle)
    elif typeOfMovement == 3:
        angle = int (sys.argv[2])
        rotateClockwise(angle)
    else:
        print("Wrong first argument")
else:
    print("All arguments have to be integers")
