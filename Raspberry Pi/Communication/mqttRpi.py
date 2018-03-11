#!/usr/bin/env python3

from bluetooth import *
import paho.mqtt.client as mqtt
import vlc
import os
import string
import random

#os.system("./")

clientPhone = mqtt.Client()
clientPhone.connect("10.42.0.1", 1883, 60000)


clientEV3 = mqtt.Client()
clientEV3.connect("10.42.0.54", 1883, 60000)


#p = vlc.MediaPlayer("/home/pi/Desktop/zelda.mp3")

# Return a random size of the sequence
def size_generator(size=1, chars="3456789"):
    return int(''.join(random.choice(chars) for _ in range(size)))

# Return a random sequence
def sequence_generator(size = size_generator(), chars="012"):
    return ''.join(random.choice(chars) for _ in range(size))
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    client.subscribe("topic/rpi/dt")
    
def on_message(client, userdata, msg):
    
    data = str(msg.payload)
    print(data)
    
    # Phone -> Rpi -> EV3
    
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
        clientEV3.publish("topic/ev3/dt", str("353,"+sequence_generator()))
        #p.play()        
    elif(data == "b'4'"):
        os.system("python3 faceDetection.py")
    elif(data == "b'-1'"):
        clientEV3.disconnect()
    
        
    # EV3 -> Rpi -> Phone
        
    else:
        print("Received")
        print(data)
        clientPhone.publish("topic/android/dt", data)
        #p.pause()
    

clientPhone.on_connect = on_connect
clientPhone.on_message = on_message
clientPhone.loop_forever()       

