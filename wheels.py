import ev3dev.ev3 as ev3
import sys
import helpers as hp
from time import sleep,time

def resetPositions():
    rWheel.position = 0
    lWheel.position = 0

def goBackwards(distance, speed=500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    rWheel.run_forever(speed_sp = -speed)
    lWheel.run_forever(speed_sp = speed)

def goForwards(distance, speed=500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = -speed)

def stop():
    rWheel, lWheel, gyroSensor = initializeSensors()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = -speed)
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")

def resetGyro():
    gyroSensor.mode = 'GYRO-RATE'
    gyroSensor.mode = 'GYRO-ANG'

def initializeSensors():
    rWheel = ev3.MediumMotor('outA')
    lWheel = ev3.MediumMotor('outB')
    gyroSensor = ev3.GyroSensor(ev3.INPUT_1)
    return (rWheel, lWheel, gyroSensor)

def rotateClockwiseAtAngle(angle, speed=-500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    while(gyroSensor.angle <= angle+1):
        print(gyroSensor.angle)
        rWheel.run_forever(speed_sp = speed)
        lWheel.run_forever(speed_sp = speed)
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")

def rotateAntiClockwiseAtAngle(angle, speed=-500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    angle = - abs(angle)
    while(gyroSensor.angle >= angle-1):
        print(gyroSensor.angle)
        rWheel.run_forever(speed_sp = speed)
        lWheel.run_forever(speed_sp = speed)
    rWheel.stop(stop_action="hold")
    lWheel.stop(stop_action="hold")

def rotateClockwise(speed=500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = speed)

def rotateAntiClockwise(speed=500):
    rWheel, lWheel, gyroSensor = initializeSensors()
    resetGyro()
    rWheel.run_forever(speed_sp = speed)
    lWheel.run_forever(speed_sp = speed)
