#!/usr/bin/env python3
# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $
'''
from bluetooth import *
from time import *
import sys

fsock = open('out.txt', 'w')
sys.stdout = sys.stderr = fsock
print("standard output")

# search for the SampleServer service
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid = uuid, address = "F0:43:47:51:71:B1" )

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

# Create the client socket
sock=BluetoothSocket( RFCOMM )
sock.listen(1)
sock.connect((host, port))
#print("connected.  type stuff")
#sock.send(bytes('Hello Andorid', 'UTF-8'))
sleep(100)
try:
    print("receiving")
    while True:
        data = sock.recv(3)
        print("received [%s]" % data.decode('utf-8'))
        if len(data) != 0:
            print("received [%s]" % data.decode('utf-8'))
            sock.close()
            exit()

except IOError:
    pass

sock.close()

'''


from bluetooth import *
import os

hostMACAddress = 'A0:E6:F8:DB:8C:21' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
#port = 3
backlog = 1
size = 1024
s = BluetoothSocket(RFCOMM)
s.bind(("", PORT_ANY))
s.listen(backlog)
print("Listening")

port = s.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

"""
advertise_service( s, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ]
                )
                """

try:
    client, clientInfo = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            os.system(str(data))
            client.send(data) # Echo back to client
except:
    print("Closing socket")
    client.close()
    s.close()
