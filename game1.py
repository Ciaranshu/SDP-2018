import ev3dev.ev3 as ev3
import sys
from time import sleep

"""
Function that sets all the motors to the position they initially were in.
Input - a list of motors to be reset
Returns - nothing
"""
def resetMotors(motors):
    while True:
        if len(motors) == 0:
            break
        toRemove = []
        # Loop through the motors and adjust their position.
        for i,motor in enumerate(motors):
            if motor.position > 0:
                motor.run_forever(speed_sp = -100)
                print( "Motor number " + str(i) + " at " + str(motor.position))
                if(motor.position <= 0):
                    motor.stop(stop_action="hold")
                    print("Remove motor " + str(i))
                    toRemove.append(motor)
                    continue
            elif motor.position < 0:
                print( "Motor number " + str(i) + " at " + str(motor.position))
                motor.run_forever(speed_sp = 100)
                if(motor.position >= 0):
                    motor.stop(stop_action="hold")
                    print(" Removing motor " + str(i))
                    toRemove.append(motor)
                    continue
            else:
                toRemove.append(motor)
                motor.stop(stop_action="hold")
                continue
        # Remove all the motors which are in the right position already.
        for mot in toRemove:
            motors.remove(mot)

lShoulder = ev3.LargeMotor('outA')
rShoulder = ev3.LargeMotor('outC')
lElbow = ev3.LargeMotor('outD')
rElbow = ev3.LargeMotor('outB')
rTouch = ev3.TouchSensor(ev3.INPUT_1)
lTouch = ev3.TouchSensor(ev3.INPUT_2)

rShoulder.position = 0
lShoulder.position = 0

rElbow.position = 0
lElbow.position = 0

saidHello = 0
saidLetsPlayGame = 0

touch1 = 0
touch2 = 0
touch3 = 0
move = int(sys.argv[1])    # Number of move to execute, given by the app 

rShoulderReset = 0
lShoulderReset = 0
rElbowReset = 0
lElbowReset = 0

while True:
   pRS = rShoulder.position # Position of Right Shoulder 
   pRE = rElbow.position    # Position of Right Elbow
   pLS = lShoulder.position # Position of Left Shoulder
   pLE = lElbow.position    # Position of Left Elbow
   
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
      if(saidLetsPlayGame == 0):
         ev3.Sound.speak("Let's play a game!")
         sleep(1.5)
         saidLetsPlayGame = 1
      # Action 2.
      rShoulder.run_forever(speed_sp =300) # rShoulder Motor Positive goes Up
      lShoulder.run_forever(speed_sp =-300)# LShoulder Motor Positive goes Down
     # rElbow.run_forever(speed_sp =-100)
     # lElbow.run_forever(speed_sp = +100)
      print("1-RIGHT-SHOULDER-UP: ",pRS)
      print("1-LEFT-SHOULDER-UP: ",pLS)
      if (pRS>450 and pLS <-450):
         rShoulder.stop(stop_action="hold")
         lShoulder.stop(stop_action="hold")
         move = 0.5
  # Action 3. 
  if (move == 0.5):          
      touch1 = touch1 + rTouch.value()
      touch2 = touch2 + lTouch.value()
      print("WAIT FOR TOUCH 1: ",touch1)
      if (touch1>0 and touch2 > 0):
         # Action 4.
         rShoulder.run_forever(speed_sp =-300)
         lShoulder.run_forever(speed_sp =+300)
         print ("2-RIGHT-SHOULDER-DOWN: ",pRS)
         if (pRS<200 and pLS > -200):
            # Action 5.
            rShoulder.stop(stop_action="hold")
            lShoulder.stop(stop_action="hold")
            ev3.Sound.speak('Well Done!')
            break
   # Say Hello and Wave Hands
   if (move == 1):  
      if(saidHello == 0):
         ev3.Sound.speak('Hello!')
         sleep(1)
         saidHello = 1
      rElbow.run_forever(speed_sp =-300) # rElbow Motor Positive goes Down 
      lElbow.run_forever(speed_sp =-300) # ...
      print("RIGHT-ELBOW-UP: ", pRE)
      print("LEFT-ELBOW-UP: ", pLE)		 
      if(pRE < -100 and pLE < -100):
         rElbow.stop(stop_action="hold")
         lElbow.stop(stop_action ="hold")
         move = 1.1
   if (move == 1.1):  
      rElbow.run_forever(speed_sp = 300) # rElbow Motor Positive goes Down 
      lElbow.run_forever(speed_sp = 300) # ...
      print("RIGHT-ELBOW-DOWN: ", pRE)
      print("LEFT-ELBOW-DOWN: ", pLE)		 
      if(pRE > 0 and pLE >0):
         rElbow.stop(stop_action="hold")
         lElbow.stop(stop_action ="hold")
         move = 1.2
   if (move == 1.2):  
      rElbow.run_forever(speed_sp =-300) # rElbow Motor Positive goes Down 
      lElbow.run_forever(speed_sp =-300) # ...
      print("RIGHT-ELBOW-UP: ", pRE)
      print("LEFT-ELBOW-UP: ", pLE)		 
      if(pRE < -100 and pLE < -100):
         rElbow.stop(stop_action="hold")
         lElbow.stop(stop_action ="hold")
         move = 1.3
   if (move == 1.3):  
      rElbow.run_forever(speed_sp = 300) # rElbow Motor Positive goes Down 
      lElbow.run_forever(speed_sp = 300) # ...
      print("RIGHT-ELBOW-DOWN: ", pRE)
      print("LEFT-ELBOW-DOWN: ", pLE)		 
      if(pRE > 0 and pLE >0):
         rElbow.stop(stop_action="hold")
         lElbow.stop(stop_action ="hold")
         break
     

print("Exited the loop")
resetMotors([rShoulder,lShoulder,lElbow, rElbow])
print("Exited the reset function.Program terminated")

#if not (rShoulder.connected):
#    print ("Plug the right shoulder motor into port C")
#else:
#    if not (rElbow.connected):
#       print ("Plug the right elbow motor into port A")
#    else:


