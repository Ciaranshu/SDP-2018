import ev3dev.ev3 as ev3
import sys
import helpers as hp
import json
import paho.mqtt.client as mqtt
from time import sleep,time

client2 = mqtt.Client()
client2.connect("10.42.0.1",1883,60000)

def initializeSensors():
    lShoulder = ev3.LargeMotor('outA')
    rShoulder = ev3.LargeMotor('outB')
    lElbow = ev3.LargeMotor('outC')
    rElbow = ev3.LargeMotor('outD')
    rTouch = ev3.TouchSensor(ev3.INPUT_1)
    lTouch = ev3.TouchSensor(ev3.INPUT_2)
    return (lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch)

def move0():
    times = []
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
    ev3.Sound.set_volume(100)
    ev3.Sound.speak("Let's play a game!")
    sleep(1.5)
    hp.setMotors([rShoulder, lShoulder],[450, -450])
    times.append(hp.waitForTouch([rTouch, lTouch], "both"))
    hp.setMotors([rShoulder, lShoulder], [0,0])
    ev3.Sound.speak('Well Done!')
    client2.publish("topic/rpi/dt",str(times))
    

# Say Hello and Wave Hands
def move1():
    
    lShoulder, rShoulder, lElbow, rElbow, rTouch, lTouch = initializeSensors()
   # ev3.Sound.speak('Hello!')
   # sleep(1)
    t = time()
    print(t)
    hp.setMotors([rElbow, lElbow],[-100, -100])
    hp.setMotors([rElbow, lElbow],[0, 0])
    hp.setMotors([rElbow, lElbow],[-100, -100])
    hp.setMotors([rElbow, lElbow],[0, 0])
    client2.publish("topic/rpi/dt","Robot said Hello Message")
#    client2.disconect()

def move2():
    times=[]
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
        times.append(hp.waitForTouch([rTouch, lTouch],"both"))
        hp.setMotors([rElbow, lElbow], [150, 150])
        hp.setMotors([rShoulder, lShoulder], [0,0])
        hp.setMotors([rShoulder, lShoulder, rElbow, lElbow] , [-250, +250, +150, +150])
        hp.setMotors([rElbow, lElbow], [0, 0])
        hp.setMotors([rShoulder, lShoulder], [0,0])
    client2.publish("topic/rpi/dt",str(times))

def press(sequence):
    lenSeq = len(sequence)
    
    print("Come play with me!")
    rTouch = ev3.TouchSensor(ev3.INPUT_1)
    lTouch = ev3.TouchSensor(ev3.INPUT_2)
    cTouch = ev3.TouchSensor(ev3.INPUT_3)
    score =0 
    buttons = [rTouch, lTouch, cTouch]
    while (len(sequence) > 0):
        nextButton = int(sequence[0])
        for i,button in enumerate(buttons):
           doneAction = False 
           while buttons[i].value() > 0:
               if (not doneAction):
                   if ( i == nextButton ):
                       sequence = sequence[1:]
                       print("Ah")
                       score+=1
                   else:
                       print("Mistakes have been done")
                       # Sends the score to rpi for the current game to rpi 
                       client2.publish("topic/rpi/dt",str("memory: " + str(score)))
                       return False
               doneAction = True
    print("Orgasm")
    # Sends a successful completion of the current game to rpi
    client2.publish("topic/rpi/dt",str("memory: " + "100")) 
    return True
#press("012")
#press(' '.join(['2' * 100]))
