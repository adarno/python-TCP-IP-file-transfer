""" client.py

    Example TCP/IP client. Not threaded.
    Got replaced by multi_client.py

"""

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8070)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:

    # open file
    file_obj = open("testfile.sat", "r")
    message = file_obj.read()
    #message = "this is a test message."

    # Send data
    print("sending: " + file_obj.name)
    sock.sendall(message)

    # close file
    file_obj.close()

    # receive response
    response = sock.recv(1024)
    print("received: " + response)

finally:
    print("closing socket.")
    sock.close()