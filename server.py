import socket
import sys
import threading
import json


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
        path = "recv/" + json_obj['file_name']

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
