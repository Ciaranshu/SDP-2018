import ev3dev.ev3 as ev3
import sys
from time import sleep

rShoulder = ev3.LargeMotor('outC')
rElbow = ev3.LargeMotor('outA')
rTouch = ev3.TouchSensor(ev3.INPUT_1)

rShoulder.position = 0
rElbow.position = 0

saidHello = 0

touch1 = 0
touch2 = 0
touch3 = 0
move = int(sys.argv[1])    # Number of moves completed 

rShoulderReset = 0
rElbowReset = 0

while True:
   pRS = rShoulder.position # Position of Right Shoulder 
   pRE = rElbow.position    # Position of Right Elbow
   if (move == 0):          
      rShoulder.run_forever(speed_sp =300) # rShoulder Motor Positive goes Up
      print("1-RIGHT-SHOULDER-UP: ",pRS)
      if (pRS>700):
         rShoulder.stop(stop_action="hold")
         move = 1
   if (move == 1):          
      touch1 = touch1+ rTouch.value()
      print("WAIT FOR TOUCH 1: ",touch1)
      if (touch1>0):
         rShoulder.run_forever(speed_sp =-300)
         print ("2-RIGHT-SHOULDER-DOWN: ",pRS)
         if (pRS<200):
            rShoulder.stop(stop_action="hold")
            move = 2
   if (move == 2):  
      touch2 = touch2 +rTouch.value()
      print("WAIT FOR TOUCH 2: ",touch2)
      if (touch2>0):
         if(saidHello ==0):
            ev3.Sound.speak('Hello darkness my old friend!')
            sleep(4)
            saidHello =1
         rElbow.run_forever(speed_sp =-300) # rElbow Motor Positive goes Down 
         print("3-RIGHT-ELBOW-UP: ", pRE) 
         if(pRE<-300):
            rElbow.stop(stop_action="hold")
            move =3
   if (move == 3):
      touch3 = touch3 +rTouch.value()
      print("WAIT FOR TOUCH 3: ", touch3)
      if(touch3>0):
         if(rElbowReset == 0):
            rElbow.run_forever(speed_sp =200)
         if(rShoulderReset == 0):
            rShoulder.run_forever(speed_sp =-200)
         print("4-RESETING-RIGHT-ELBOW",pRE)
         print("4-RESETING-RIGHT-SHOULDER",pRS)
         if(pRE>0):
            rElbow.stop(stop_action="hold")
            rElbowReset =1
         if(pRS<0):
            rShoulder.stop(stop_action="hold")
            rShoulderReset =1
         if(rShoulderReset==1 and rElbowReset==1):
            move=4
   if (move == 4):
      print("Finished all moves!")
      break


#if not (rShoulder.connected):
#    print ("Plug the right shoulder motor into port C")
#else:
#    if not (rElbow.connected):
#       print ("Plug the right elbow motor into port A")
#    else:


