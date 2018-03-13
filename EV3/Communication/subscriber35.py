#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import game1
import helpers as hp
from time import time
from ev3dev.auto import *

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/ev3/dt")

def on_message(client, userdata, msg):
    data = str(msg.payload)
    if (len(data)>6):
        #play memory game
        #expecting a message of form "b'353,XXXXX'"
        #XXXX denotes the sequence of buttons, X is 0, 1 or 2
        (code, sequence) = data.split(",") # Split data on comma
        sequence = sequence[:-1] # Just to remove the ' at the end of the sequence
        print(sequence)
        game1.press(sequence)
        
    elif(data == "b'350'"):
        game1.move0()

    elif(data == "b'351'"):
        game1.move1()

    elif(data == "b'352'"):
        game1.move2()

client = mqtt.Client()
client.connect("10.42.0.54",1883,60000)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
