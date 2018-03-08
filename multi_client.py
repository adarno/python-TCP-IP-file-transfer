""" multi_client.py

    TCP/IP client that can handle multiple connections. Connects with server.py.

    Reads data from file and sends json object to server containing data, the name of the client
    as well as the name of the transferred file.

"""


import socket
import threading
import json


class ClientThread(threading.Thread):

    def __init__(self, server_port, file_name, client_name):
        super(ClientThread, self).__init__()
        self.file_name = file_name
        self.client_name = client_name
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
            file_obj = open(self.file_name, "r")

            # set up dictionary
            message_dict = {"client"    : self.client_name,
                            "file_name" : self.file_name,
                            "data"      : file_obj.read()}

            # convert dictionary to json
            json_message = json.dumps(message_dict)

            # Send data
            print(self.name + ": sending: " + file_obj.name + "\n")

            # close file
            file_obj.close()

            self.socket.sendall(json_message)

            # receive response
            response = self.socket.recv(1024)
            print(self.name + ": received: " + response)

        finally:
            print(self.name + ": closing socket.")
            self.socket.close()




thread1 = ClientThread(8070, "testfile.sat", "name1")
thread2 = ClientThread(8070, "sat_example.sat", "name2")

# start threads
thread1.start()
thread2.start()

