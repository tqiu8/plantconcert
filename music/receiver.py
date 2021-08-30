#!/usr/bin/env python3

import socket
import sys

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
# host, port = '192.168.1.61', 65000
host, port = "0.0.0.0", 65000
server_address = (host, port)

print('Starting UDP server on {host} port {port}').format(host=host, port=port)
sock.bind(server_address)

while True:
    # Wait for message
    message, address = sock.recvfrom(1024)
    message = message.decode()
    print("message", message)