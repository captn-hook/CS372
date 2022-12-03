# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(host, port):
    #create socket
    server_socket = socket.socket()
    try:
        server_socket.bind((host, port))
    except:
        print("Unable to bind to host/port")
        return 1
    
   
    server_socket.listen()

    sockset = {server_socket}
    print("*** Server starting")
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

def usage():
    print("usage: chat_server.py host port", file=sys.stderr)
    
def main(argv):
    try:
        host = argv[1]
        port = int(argv[2])
    except:
        usage()
        return 1
            
    
    run_server(host, port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
