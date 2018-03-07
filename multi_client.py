import socket
import sys
import threading


class ClientThread(threading.Thread):

    def __init__(self, server_port, message):
        super(ClientThread, self).__init__()
        self.message = message
        self.port = server_port

        # Create a TCP/IP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.server_address = ('localhost', self.port)
        print(self.name + ': connecting to %s port %s' % self.server_address)
        self.socket.connect(self.server_address)

    def run(self):
        try:

            # open file
            #file_obj = open("testfile.sat", "r")
            #message = file_obj.read()
            # message = "this is a test message."

            # Send data
            #print("sending: " + file_obj.name)

            # close file
            #file_obj.close()

            self.socket.sendall(self.message)

            # receive response
            response = self.socket.recv(1024)
            print(self.name + ": received: " + response)

        finally:
            print(self.name + ": closing socket.")
            self.socket.close()




thread1 = ClientThread(8070, "message 1")
thread2 = ClientThread(8070, "message 2")

# start threads
thread1.start()
thread2.start()

