import time
import board
from digitalio import DigitalInOut, Direction
import socket
import sys
import random
from struct import pack

board_name = "bluewave"
# set the GPIO input pins
pad0_pin = board.D22
pad1_pin = board.D21
pad2_pin = board.D17
pad3_pin = board.D24
pad4_pin = board.D23

pins = [pad0_pin, pad1_pin, pad2_pin, pad3_pin, pad4_pin]
pads = [DigitalInOut(p) for p in pins]
pad_already_pressed = [True for p in pads]
names = ["fiddle0", "fiddle1", "rubber0", "rubber1", "philo0"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host, port = "192.168.1.19", 65000
server_address = (host, port)
pressed = False
sensor = 0
previous_state = [p.value for p in pads]
while True:
    current_state = [p.value for p in pads]
    delta = [i for i in range(len(current_state)) if previous_state[i] != current_state[i]]
    if len(delta) > 0:
        sensor = sum(delta)
        pressed = not pressed
    if pressed:
         print("pressed", delta, sensor)
    else:
        print("not pressed", delta)
    """
    for i, pad in enumerate(pads):
        if pad.value and not pad_already_pressed[i]:
        #if pad.value:
            name = names[i]
            print("{name} pressed".format(name = name))
            message = bytes("{board_name}-{name}".format(board_name=board_name, name=name), 'UTF-8')
            sock.sendto(message, server_address)
        #pad_already_pressed[i] = pad.value
        #cycle[i] = pad.value
    """
    previous_state = current_state
    time.sleep(0.1)
