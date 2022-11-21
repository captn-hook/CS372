# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select


def run_server(port):
    #create socket
    server_socket = socket.socket()
    server_socket.bind(('127.0.0.1', port))
    
    server_socket.listen()

    sockset = {server_socket}

    while True:
        #wait for input

        input_ready, output_ready, except_ready = select.select(sockset, [], [])

        for sock in input_ready:
            if sock == server_socket:
                #accept connection
                new_sock, connection_info = server_socket.accept()

                sockset.add(new_sock)

                print(f"{new_sock.getpeername()}: connected")

            else:
                #receive data
                data = sock.recv(1024)

                name = sock.getpeername()

                if data:

                    data = data.decode()

                    print(f"{name}: {len(data)} bytes: {data}")

                else:
                    
                    print(f"{sock.getpeername()}: disconnected")

                    sock.close()

                    sockset.remove(sock)


    #
    #main loop:
    #
    #    call select() and get the sockets that are ready to read
    #
    #    for all sockets that are ready to read:
    #
    #        if the socket is the listener socket:
    #            accept() a new connection
    #            add the new socket to our set!
    #
    #        else the socket is a regular socket:
    #            recv() the data from the socket
    #
    #            if you receive zero bytes
    #                the client hung up
    #                remove the socket from the set!
    #
    #socket.getpeername()

    
#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
