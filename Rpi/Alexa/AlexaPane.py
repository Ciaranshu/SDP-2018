from flask import Flask
from flask_ask import Ask, statement, convert_errors
import logging
from bluetooth import *
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
#from os import system as sys
import subprocess
from /home/pi/SDP-2018/Rpi/Communication/mqttRpi.py import lights

clientEV3 = mqtt.Client()


GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

flag = True

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
print ("running")

def sequence_generator(chars="012",*,size, game):
    global pattern
    if ((game % 3) == 0):
        pattern += str(''.join(random.choice(chars) for _ in range(size)))
    elif ((game % 3) == 1):
        pattern = str(''.join(random.choice(chars) for _ in range(size)))
    elif ((game % 3) == 2):
        pattern = str(''.join(random.choice(chars) for _ in range(size)))

@ask.intent('SetupLeo')
def setup():
    print ("Automatically Setup:")
    try:
        subprocess.call("sudo -u pi python /home/pi/SDP-2018/Rpi/Communication/initialisationScript.py")
        return statement('Leo has set up')
    except:
        return statement('Fail to set up Leo, please try it again')

@ask.intent('ConnectLeo')
def connection():
    print("Connect Leo to Phone:")
    try:
        subprocess.call("sudo -u pi python3 /home/pi/SDP-2018/Rpi/Communication/mqttRpi.py")
        return statement('Connecting to Leo')
    except:
        return statement('Fail to connect to Leo, please try it again')

@ask.intent('FaceMe')
def faceDetection():
    print("Make Leo Face to User:")
    try:
	subprocess.call("sudo -u pi python3 /home/pi/SDP-2018/Rpi/FaceDetection/faceDetection.py")
        return statement('Leo found you')
    except:
        return statement('Leo was fail to find you, please try it again')


@ask.intent('trick', mapping={'trick':'trick'})
def reaction_game(trick):
    global flag
    if flag:
        clientEV3.connect("10.42.0.54", 1883, 60000)
        flag = False
    if trick == 'hello':
	clientEV3.publish("topic/ev3/dt", "351")

@ask.intent('memoryGame', mapping={'mode':'mode'})
def reaction_game(mode):
    global pattern
    global flag
    if flag:
        clientEV3.connect("10.42.0.54", 1883, 60000)
        flag = False
    elif game == "memorize" or "memory":
        if mode == "very easy":
            game = 2
            sequence_generator(size=5, game=game)
            lights(pattern)
            clientEV3.publish("topic/ev3/dt", str("356,"+pattern))

        elif mode == "easy":
            game = 0
            sequence_generator(size=2, game=game)
            lights(pattern)
            clientEV3.publish("topic/ev3/dt", str("356,"+pattern))

        elif mode == "normal":
            game = 5
            sequence_generator(size=5, game=game)
            lights(pattern)
            clientEV3.publish("topic/ev3/dt", str("357,"+pattern))

        elif mode == "hard":
            game = 1
            sequence_generator(size=2, game=game)
            lights(pattern)
            clientEV3.publish("topic/ev3/dt", str("356,"+pattern))

        elif mode == "very hard":
            game = 3
            sequence_generator(size=2, game=game)
            lights(pattern)
            clientEV3.publish("topic/ev3/dt", str("357,"+pattern))

        elif mode == "prestige":
            game = 4
            sequence_generator(size=2 ,game=game)
            lights(pattern)
            clientEV3.publish("topic/ev3/dt", str("357,"+pattern))

        else:
            return statement ('I do not know this game')
        return statement('Playing {} game'.format(mode))

@ask.intent('reactionGame', mapping={'game': 'game', 'num': 'num'})
def reaction_game(game, num):
    global flag
    if flag:
	clientEV3.connect("10.42.0.54", 1883, 60000)
	flag = False

    print ("playing game:", mode, game, num)
    if game == 'reaction':
	print ("playing reaction game", int(num))
        if int(num) == 0:
            clientEV3.publish("topic/ev3/dt", "350")
	elif int(num) == 1:
	    clientEV3.publish("topic/ev3/dt", "352")
        elif int(num) == 2:
            clientEV3.publish("topic/ev3/dt", "353")
        elif int(num) == 3:
            clientEV3.publish("topic/ev3/dt", "354")
        elif int(num) == 4:
            clientEV3.publish("topic/ev3/dt", "355")
	else:
	    return statement ('I do not know this game')
    else:
	return statement ('I do not know this game')
    return statement('Playing {} game'.format(game))

if __name__ == '__main__':
    port = 5000
    app.run(host='127.0.0.1', port = port)
