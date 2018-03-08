""" server.py

    TCP/IP server that opens a new thread for every new connection.
    Received data should be a json object of type
    {"client": client_name, "file_name": name_of_file, "data": data_contained_in _file}.

    Server creates a new directory for every client specified by the name of the client
    in /recv and writes the client's data to that directory.
"""

import socket
import sys
import threading
import json
import datetime
import os


class ServerThread(threading.Thread):

    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.client_address = client_address
        self.client_socket = client_socket
        print(self.name + ": [+] New thread started for " + str(self.client_address))

    def run(self):

        raw_data = ""

        try:
            print >> sys.stderr, 'connection from', self.client_address

            print(self.name + ": receiving data ...")
            # Receive the data in small chunks
            while True:
                data = self.client_socket.recv(1024)

                if data:
                    raw_data += data
                    response = "transfer successfull"
                    try:
                        self.client_socket.send(response)
                    except:
                        pass
                else:
                    print(self.name + ": " + self.client_socket + " closed the connection.")
                    break


        except:
            # Clean up the connection
            self.client_socket.close()

        # convert raw_data to json
        json_obj = json.loads(raw_data)

        # create timestamp
        timestamp = datetime.date.today().strftime("%Y_%m_%d_")
        timestamp += datetime.datetime.today().strftime("%H%M%S")

        # ckeck whether client directory exists
        if not os.path.isdir("recv/" + json_obj['client']):
            os.mkdir("recv/" + json_obj['client'])

        # timestamp directory should not exist yet but check for safety purposes
        if not os.path.isdir("recv/" + json_obj['client'] + "/" + str(timestamp)):
            os.mkdir("recv/" + json_obj['client'] + "/" + str(timestamp))

        # asseble path where file will be written
        path = "recv/" + json_obj['client'] + "/" \
               + str(timestamp) + "/" + json_obj['file_name']

        # write data to file
        file_obj = open(path, "w")
        print(self.name + ": writing data to file")
        file_obj.write(json_obj['data'])
        file_obj.close()


if __name__ == "__main__":

    host = "127.0.0.1"
    port = 8070

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcpsock.bind((host,port))
    threads = []

    while True:

        tcpsock.listen(4)
        print "\nListening for incoming connections..."
        connection, client_address = tcpsock.accept()

        # open new thread for connection and start
        new_thread = ServerThread(client_address, connection)
        new_thread.start()

        threads.append(new_thread)
