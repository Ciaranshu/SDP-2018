import ev3dev.ev3 as ev3
import sys
import helpers as hp
import json
from time import sleep,time

def initializeSensors():
    lShoulder = ev3.LargeMotor('outA')
    rShoulder = ev3.LargeMotor('outB')
    lElbow = ev3.LargeMotor('outC')
    rElbow = ev3.LargeMotor('outD')
    rTouch = ev3.TouchSensor(ev3.INPUT_1)
    lTouch = ev3.TouchSensor(ev3.INPUT_2)
    return (lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch)

def move0():
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    ev3.Sound.set_volume(100)
    ev3.Sound.speak("Let's play a game!")
    sleep(1.5)
    hp.setMotors([rShoulder, lShoulder],[450, -450])
    hp.waitForTouch([rTouch, lTouch])
    hp.setMotors([rShoulder, lShoulder], [0,0])
    ev3.Sound.speak('Well Done!')

# Say Hello and Wave Hands
def move1():
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    ev3.Sound.speak('Hello!')
    sleep(1)
    hp.setMotors([rElbow, lElbow],[-100, -100])
    hp.setMotors([rElbow, lElbow],[0, 0])
    hp.setMotors([rElbow, lElbow],[-100, -100])
    hp.setMotors([rElbow, lElbow],[0, 0])

def move2():
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    t1 = time()
    for i in range(5):
        hp.setMotors([rShoulder, lShoulder], [-300, +300])
        hp.setMotors([rShoulder, lShoulder], [+550, -550])
        hp.setMotors([rShoulder, lShoulder], [0, 0])
        hp.setMotors([rElbow, lElbow], [-150, -150])
        hp.setMotors([rElbow, lElbow], [0, 0])
        hp.setMotors([rElbow, lElbow], [150, 150])
        hp.setMotors([rShoulder, lShoulder, rElbow, lElbow] , [+550, -550, -150, -150])
        hp.waitForTouch([rTouch, lTouch])
        hp.setMotors([rElbow, lElbow], [150, 150])
        hp.setMotors([rShoulder, lShoulder], [0,0])
        hp.setMotors([rShoulder, lShoulder, rElbow, lElbow] , [-250, +250, +150, +150])
        hp.setMotors([rElbow, lElbow], [0, 0])
        hp.setMotors([rShoulder, lShoulder], [0,0])
    t2 = time()
    data = {}
    finalTime = float(str(t2-t1))
    data["time"] = finalTime
    with open('time.json', 'w') as outfile:
        json.dump(data, outfile)
