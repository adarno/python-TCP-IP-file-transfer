import socket
import sys
import threading




# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 8070)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    text = ""

    try:
        print >> sys.stderr, 'connection from', client_address

        # Receive the data in small chunks
        while True:
            data = connection.recv(1024)
            print("received data ... ")

            if data:
                text += data
                response = "transfer successfull"
                try:
                    connection.send(response)
                except:
                    print("connection closed by client")
            else:
                print(client_address + " closed the connection.")
                break


    except:
        # Clean up the connection
        connection.close()

    # write data to file
    file_obj = open("recv.sat", "w")
    file_obj.write(text)
    file_obj.close()