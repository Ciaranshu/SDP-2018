#!/usr/bin/env python3

from bluetooth import *
import paho.mqtt.client as mqtt
import vlc
import os

#os.system("./")

clientSendPhone = mqtt.Client()
clientSendPhone.connect("10.42.0.1", 1883, 60000)

clientRecPhone = mqtt.Client()
clientRecPhone.connect("10.42.0.1", 1883, 60000)

clientSendEV3 = mqtt.Client()
clientSendEV3.connect("10.42.0.54", 1883, 60000)

#clientRecEV3 = mqtt.Client()
#clientRecEV3.connect("10.42.0.1", 1883, 60)

#p = vlc.MediaPlayer("/home/pi/Desktop/zelda.mp3")
 
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    client.subscribe("topic/motor-A/dt")
    
def on_connect2(client, userdata, flags, rc):
    print("Connected with result code " +str(rc))
    client.subscribe("topic/getMessage35/dt")
    
def on_message(client, userdata, msg):
    
    data = str(msg.payload)
    print(data)
    
    # Rpi -> EV3
    
    if(data == "b'0'"):
        clientSendEV3.publish("topic/motor-A/dt", "350")
        #p.play()
    elif(data == "b'1'"):
        clientSendEV3.publish("topic/motor-A/dt", "351")
        #p.play()
    elif(data == "b'2'"):
        clientSendEV3.publish("topic/motor-A/dt", "352")
        #p.play()
    elif(data == "b'3'"):
        os.system("python3 faceDetection.py")
    elif(data == "b'-1'"):
        clientSendEV3.disconnect()
    
    elif(data == "b'350'" or data == "b'351'" or data == "b'352'" ):
        print("Ignore")
        
    # Rpi -> Phone
        
    else:
        print("Received")
        print(data)
        clientSendPhone.publish("topic/android/dt", data)
        p.pause()
    

    
    
        
def on_message2(client, userdata, msg):
    data = msg.payload.decode()
    print(data)



#clientRecEV3.on_connect = on_connect
#clientRecEV3.on_message2 = on_message2

clientRecPhone.on_connect = on_connect
clientRecPhone.on_message = on_message

#clientRecEV3.loop_forever()
clientRecPhone.loop_forever()       

#clientSendPhone.on_connect = on_connect
#clientSendPhone.on_message = on_message

#clientSendPhone.loop_forever()
