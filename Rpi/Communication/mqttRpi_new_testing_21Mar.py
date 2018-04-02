#!/usr/bin/env python3

from bluetooth import *
import paho.mqtt.client as mqtt
import vlc
import os
import string
import random
import RPi.GPIO as GPIO
import time

#os.system("./")
def lights(seq):
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    # pins for the + of the circuit
    pins = [36, 22, 32]
    # the closest grounds are [14,20,34]
    for digit in seq:
        num = pins[int(digit)]
        print(num)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(num,GPIO.OUT)
        GPIO.output(num,1)
        time.sleep(1)
        GPIO.output(num,0)
        time.sleep(1)

#lights("021021")

flag =  True
pattern =""
score =0

clientPhone = mqtt.Client()
clientPhone.connect("10.42.0.1", 1883, 60000)



clientEV3 = mqtt.Client()
clientEV3.connect("10.42.0.54", 1883, 60000)


p = vlc.MediaPlayer("/home/pi/Desktop/zelda.mp3")

# Formula to return the divisor : (n^2 * n) / 2
def formula(outOf):
    return int((((outOf*outOf)+outOf)/2)-1)

# Return a random sequence
def sequence_generator(size = 2, chars="012"):
    global pattern
    pattern += str(''.join(random.choice(chars) for _ in range(size)))
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    client.subscribe("topic/rpi/dt")
    
def on_message(client, userdata, msg):
    global pattern
    global score
    global flag
    data = str(msg.payload)
    print(data)
    ######### Phone -> Rpi -> EV3 #########
    
    if(data == "b'0'" and flag):
        flag = False
        clientEV3.publish("topic/ev3/dt", "350")
        #p.play()
    elif(data == "b'1'" and flag):
        flag = False
        clientEV3.publish("topic/ev3/dt", "351")
        #p.play()
    elif(data == "b'2'" and flag):
        flag = False
        clientEV3.publish("topic/ev3/dt", "352")
        #p.play()
    elif(data == "b'3'" and flag):
        flag = False
        # p.play()
        # Memory game
        sequence_generator()
        lights(pattern)
        clientEV3.publish("topic/ev3/dt", str("353,"+pattern))
        #p.play()        
    elif(data == "b'4'" and flag):
        flag = True  # We should add a stop button on the app so we can be able to turn the flag on again since the  ev3(15) is no communicating with the script 
        os.system("python3 faceDetection.py")
    elif(data == "b'-1'" and flag):
        flag = True
        clientEV3.disconnect()
    
    ####### Memory part #######
    
    # If the user completes current stage
    elif(data == "b'memory: 100'"):
       
        # Update score
        score+=len(pattern)
        
        # Stop when the size of the pattern is larger than 10, which is dettermined he last stage
        if(len(pattern) >=10):
           # p.pause()
            
            # Sending results to app after successful completion of game eg. Score 55/55
            clientPhone.publish("topic/android/dt", "b'Score: "+str(score)+ "/" + str(formula(len(pattern))))
            
            # Resetting pattern and score 
            pattern=""
            score = 0
            flag = True
            
        else:
            
            # Add one random touch to the pattern
            sequence_generator(1)
            
            lights(pattern)
            # Run the new pattern on EV3
            clientEV3.publish("topic/ev3/dt", str("353,"+pattern))
        
    # If the user fails to complete the current stage    
    elif(data[:9] == "b'memory:"):
        p.pause()
        
        #Update score
        score+=int(data[10:len(data)-1])
        
        # Sending results to app after a wrong touch eg. Score 6/9
        clientPhone.publish("topic/android/dt", "b'Score: "+str(score)+ "/" + str(formula(len(pattern))))
        
        # Resetting pattern and score 
        pattern=""
        score = 0
        flag = True
        

    ###### EV3 -> Rpi -> Phone ######
        
    else:
        print("Received")
        print(data)
        clientPhone.publish("topic/android/dt", data)
        #p.pause()
        flag = True
    

clientPhone.on_connect = on_connect
clientPhone.on_message = on_message
clientPhone.loop_forever()
