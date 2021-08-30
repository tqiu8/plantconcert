import time
import board
from digitalio import DigitalInOut, Direction
import socket
import sys
import random
from struct import pack

plant_name = "monstera"
# set the GPIO input pins
pad0_pin = board.D22
pad1_pin = board.D21
pad2_pin = board.D17
pad3_pin = board.D24
pad4_pin = board.D23

pins = [pad0_pin, pad1_pin, pad2_pin, pad3_pin, pad4_pin]
pads = [DigitalInOut(p) for p in pins]
pad_already_pressed = [True for p in pads]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host, port = "192.168.1.19", 65000
server_address = (host, port)

while True:
    for i, pad in enumerate(pads):
        if pad.value and not pad_already_pressed[i]:
            print("Pad {i} pressed".format(i = i))
            message = bytes("monstera-{i}".format(i=i), 'UTF-8')
            sock.sendto(message, server_address)
        pad_already_pressed[i] = pad.value
    time.sleep(0.1)
