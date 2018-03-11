#!/usr/bin/env python3

from bluetooth import *
import paho.mqtt.client as mqtt
import vlc
import os
import string
import random

#os.system("./")

pattern =""
score =0

clientPhone = mqtt.Client()
clientPhone.connect("10.42.0.1", 1883, 60000)


clientEV3 = mqtt.Client()
clientEV3.connect("10.42.0.54", 1883, 60000)


#p = vlc.MediaPlayer("/home/pi/Desktop/zelda.mp3")

# Formula to return the divisor 
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
    data = str(msg.payload)
    print(data)
    
    ######### Phone -> Rpi -> EV3 #########
    
    if(data == "b'0'"):
        clientEV3.publish("topic/ev3/dt", "350")
        #p.play()
    elif(data == "b'1'"):
        clientEV3.publish("topic/ev3/dt", "351")
        #p.play()
    elif(data == "b'2'"):
        clientEV3.publish("topic/ev3/dt", "352")
        #p.play()
    elif(data == "b'3'"):
        # Memory game
        sequence_generator()
        clientEV3.publish("topic/ev3/dt", str("353,"+pattern))
        #p.play()        
    elif(data == "b'4'"):
        os.system("python3 faceDetection.py")
    elif(data == "b'-1'"):
        clientEV3.disconnect()
    
    ####### Memory part #######
    
    elif(data == "b'memory: 100'"):
       
        # Update score
        score+=len(pattern)
        
        # Stop when the size of the pattern is larger than 10
        if(len(pattern) >=10):
            
            # Sending results to app after successful completion of game eg. Score 55/55
            clientPhone.publish("topic/android/dt", "b'Score: "+str(score)+ "/" + str(formula(len(pattern))))
            
            # Resetting pattern and score 
            pattern=""
            score = 0
            
        else:
            
            # Add one random touch to the pattern
            sequence_generator(1)
            
            # Run the new pattern on EV3
            clientEV3.publish("topic/ev3/dt", str("353,"+pattern))
        
    elif(data[:9] == "b'memory:"):
        
        #Update score
        score+=int(data[10:len(data)-1])
        
        # Sending results to app after a wrong touch eg. Score 6/9
        clientPhone.publish("topic/android/dt", "b'Score: "+str(score)+ "/" + str(formula(len(pattern))))
        
        # Resetting pattern and score 
        pattern=""
        score = 0
        

    ###### EV3 -> Rpi -> Phone ######
        
    else:
        print("Received")
        print(data)
        clientPhone.publish("topic/android/dt", data)
        #p.pause()
    

clientPhone.on_connect = on_connect
clientPhone.on_message = on_message
clientPhone.loop_forever() 