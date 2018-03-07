import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:

    # Send data
    message = 'This is the message.  It will be repeated.'
    print("sending message: " + message)
    sock.sendall(message)


    response = sock.recv(16)
    print("received: " + response)

finally:
    print("closing socket.")
    sock.close()