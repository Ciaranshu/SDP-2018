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
    message = msg.payload.strip().split(" ")
    if len(message) == 2:
        if (message[0].isalpha()):
            client.disconnect()
        elif (int(message[0]) == 0):
            wheels.goBackwards(int(message[1]))
        elif (int(message[0]) == 1):
            wheels.goForwards(int(message[1]))
        elif (int(message[0]) == 2):
            wheels.rotateClockwise(int(message[1]))
        elif (int(message[0]) == 3):
            wheels.rotateAntiClockwise(int(message[1]))

client = mqtt.Client()
client.connect("192.168.44.155",1883,60)

client.on_connect = on_connect
client.on_message = on_message

#m.run_direct()
#m.duty_cycle_sp=0

client.loop_forever()
