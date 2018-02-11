import ev3dev.ev3 as ev3
import sys
import helpers as hp
from time import sleep

lShoulder = ev3.LargeMotor('outA')
rShoulder = ev3.LargeMotor('outC')
lElbow = ev3.LargeMotor('outD')
rElbow = ev3.LargeMotor('outB')
rTouch = ev3.TouchSensor(ev3.INPUT_1)
lTouch = ev3.TouchSensor(ev3.INPUT_2)
ev3.Sound.set_volume(100)

rShoulder.position = 0
lShoulder.position = 0

rElbow.position = 0
lElbow.position = 0

move = int(sys.argv[1])    # Number of move to execute, given by the app

while True:
   """
   At this point, move = 0 does the following sequence of moves:
   1. The Robot says "Let's play a game"
   2. The Robot raises both its arms
   3. The Robot waits the player to hit both its hands.
   4. The Robot lowers its arms
   5. The Robot says "Well done!"
   """
   # Action 1.
   if (move == 0):
      ev3.Sound.speak("Let's play a game!")
      sleep(1.5)
      hp.setMotors([rShoulder, lShoulder],[450, -450])
      hp.waitForTouch([rTouch, lTouch])
      hp.setMotors([rShoulder, lShoulder], [0,0])
      ev3.Sound.speak('Well Done!')
      break
   # Say Hello and Wave Hands
   if (move == 1):
      ev3.Sound.speak('Hello!')
      sleep(1)
      hp.setMotors([rElbow, lElbow],[-100, -100])
      hp.setMotors([rElbow, lElbow],[0, 0])
      hp.setMotors([rElbow, lElbow],[-100, -100])
      hp.setMotors([rElbow, lElbow],[0, 0])
      break


print("Exited the loop")
hp.resetMotors([rShoulder,lShoulder,lElbow, rElbow])
print("Exited the reset function.Program terminated")

#if not (rShoulder.connected):
#    print ("Plug the right shoulder motor into port C")
#else:
#    if not (rElbow.connected):
#       print ("Plug the right elbow motor into port A")
#    else:
