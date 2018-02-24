#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import helpers as hp
import wheels
from ev3dev.auto import *


# This is the Subscriber
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic/motor-A/dt")

def on_message(client, userdata, msg):
    if (msg.payload.isalpha()):
        client.disconnect()
    elif (int(msg.payload) == 0):
        wheels.goForwards()
    elif (int(msg.payload) == 1):
        wheels.goBackwards()
    elif (int(msg.payload) == 2):
        wheels.rotateClockwise
    elif (int(msg.payload) == 3):
        wheels.rotateAntiClockwise
    elif (int(msg.payload) == 4):
        wheels.stop()


client = mqtt.Client()
client.connect("192.168.44.155",1883,60)

client.on_connect = on_connect
client.on_message = on_message

#m.run_direct()
#m.duty_cycle_sp=0

client.loop_forever()
