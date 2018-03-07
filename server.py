import socket
import sys
import threading


class ServerThread(threading.Thread):

    def __init__(self, client_ip, client_port, client_socket):
        threading.Thread.__init__(self)
        self.client_ip = client_ip
        self.client_port = client_port
        self.client_socket = client_socket
        print "[+] New thread started for "+ip+":"+str(port)

    def run(self):

        while True:

            text = ""

            try:
                print >> sys.stderr, 'connection from', self.client_ip, ":", self.client_port

                # Receive the data in small chunks
                while True:
                    data = self.client_socket.recv(1024)
                    print("received data ... ")

                    if data:
                        text += data
                        response = "transfer successfull"
                        try:
                            self.client_socket.send(response)
                        except:
                            pass
                    else:
                        print(self.client_socket + " closed the connection.")
                        break


            except:
                # Clean up the connection
                self.client_socket.close()

            # write data to file
            file_obj = open("recv.sat", "w")
            print("writing data to file")
            file_obj.write(text)
            file_obj.close()


if __name__ == "__main__":

    host = "127.0.0.1"
    port = 8070

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcpsock.bind((host,port))
    threads = []

    tcpsock.listen(4)
    print "\nListening for incoming connections..."
    (clientsock, (ip, port)) = tcpsock.accept()
    newthread = ServerThread(ip, port, clientsock)
    newthread.start()
    threads.append(newthread)