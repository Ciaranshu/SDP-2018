#!/usr/bin/env python3

from bluetooth import *
import paho.mqtt.client as mqtt
import vlc
import os

#os.system("./")

clientPhone = mqtt.Client()
clientPhone.connect("10.42.0.1", 1883, 60000)


clientEV3 = mqtt.Client()
clientEV3.connect("10.42.0.54", 1883, 60000)


#p = vlc.MediaPlayer("/home/pi/Desktop/zelda.mp3")
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    client.subscribe("topic/motor-A/dt")
    
def on_message(client, userdata, msg):
    
    data = str(msg.payload)
    print(data)
    
    # Phone -> Rpi -> EV3
    
    if(data == "b'0'"):
        clientEV3.publish("topic/motor-A/dt", "350")
        print("sending")
        #p.play()
    elif(data == "b'1'"):
        clientEV3.publish("topic/motor-A/dt", "351")
        #p.play()
    elif(data == "b'2'"):
        clientEV3.publish("topic/motor-A/dt", "352")
        #p.play()
    elif(data == "b'3'"):
        os.system("python3 faceDetection.py")
    elif(data == "b'-1'"):
        clientEV3.disconnect()
    
    elif(data == "b'350'" or data == "b'351'" or data == "b'352'" ):
        print("Ignore")
        
    # EV3 -> Rpi -> Phone
        
    else:
        print("Received")
        print(data)
        clientPhone.publish("topic/android/dt", data)
        #p.pause()
    

clientPhone.on_connect = on_connect
clientPhone.on_message = on_message
clientPhone.loop_forever()       

