import ev3dev.ev3 as ev3
import sys
import helpers as hp
from time import sleep,time

lShoulder = ev3.LargeMotor('outA')
rShoulder = ev3.LargeMotor('outB')
lElbow = ev3.LargeMotor('outC')
rElbow = ev3.LargeMotor('outD')
rTouch = ev3.TouchSensor(ev3.INPUT_1)
lTouch = ev3.TouchSensor(ev3.INPUT_2)
ev3.Sound.set_volume(100)

move = int(sys.argv[1])    # Number of move to execute, given by the app
   # Action 1.
if (move == 0):
    ev3.Sound.speak("Let's play a game!")
    sleep(1.5)
    hp.setMotors([rShoulder, lShoulder],[450, -450])
    hp.waitForTouch([rTouch, lTouch])
    hp.setMotors([rShoulder, lShoulder], [0,0])
    ev3.Sound.speak('Well Done!')
# Say Hello and Wave Hands
elif (move == 1):
    ev3.Sound.speak('Hello!')
    sleep(1)
    hp.setMotors([rElbow, lElbow],[-100, -100])
    hp.setMotors([rElbow, lElbow],[0, 0])
    hp.setMotors([rElbow, lElbow],[-100, -100])
    hp.setMotors([rElbow, lElbow],[0, 0])
elif (move == 2):
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
    print("Game finished successfully. Took " + str(t2-t1))

hp.resetMotors([rShoulder,lShoulder,lElbow, rElbow])
print("Exited the reset function.Program terminated")

#if not (rShoulder.connected):
#    print ("Plug the right shoulder motor into port C")
#else:
#    if not (rElbow.connected):
#       print ("Plug the right elbow motor into port A")
#    else:
