#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import game1
import helpers as hp
from ev3dev.auto import *

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/motor-A/dt")

def on_message(client, userdata, msg):
    if (msg.payload.isalpha()):
        client.disconnect()
    elif (int(msg.payload) == 0):
        game1.move0()
    elif (int(msg.payload) == 1):
        game1.move1()
    elif (int(msg.payload) == 2):
        game1.move2()

client = mqtt.Client()
client.connect("192.168.44.155",1883,60)

client.on_connect = on_connect
client.on_message = on_message

#m.run_direct()
#m.duty_cycle_sp=0

client.loop_forever()
