# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select
import json

server_socket = None

packet_buffer = {}

def run_server(host, port):

    global server_socket
    global packet_buffer

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

    users = {}
    while True:
        #wait for input

        input_ready, output_ready, except_ready = select.select(sockset, [], [])

        for sock in input_ready:
            if sock == server_socket:
                #accept connection
                new_sock, connection_info = server_socket.accept()

                sockset.add(new_sock)

                print(f"*** {new_sock.getpeername()}: connected")

            else:
                try:
                    #receive data
                    data = sock.recv(2)
                    #if data bytes < 1024, then we have a full message
                    if int.from_bytes(data, 'big') < 1024:
                        data = sock.recv(1024)
                        
                        name = sock.getpeername()

                        name = f"{name[0]}:{name[1]}"

                        if data:

                            data =  json.loads(data.decode())

                            if data["type"] == "hello":
                                print(f"*** {name}: {len(data)} bytes: {data['type']}: {data['nick']}")
                                
                                try:
                                    try:
                                        key = next(key for key, value in users.items() if value == data['nick'])
                                        print(f"*** {name}: {data['nick']} already in use by {key}")
                                        remove(sock, sockset)

                                    except StopIteration:
                                        n = users[name]

                                except KeyError:
                                    users[name] = data['nick']
                                    packet_buffer[name] = b''
                                    print(f"{name}: {users[name]}> connected")

                                    msg = {
                                        "type": "join",
                                        "nick": data['nick']
                                    }

                                    for s in sockset:
                                        if s != server_socket and s != sock:
                                            s.sendall(json.dumps(msg, indent=0).encode())

                            

                            elif users[name]:

                                nick = users[name]                   

                                print(f"{name}: {nick}> {data['message']}")

                                msg = {
                                    "type": "chat",
                                    "nick": nick,
                                    "message": data["message"]
                                }

                                msg = json.dumps(msg, indent=0).encode()

                                for s in sockset:
                                    if s != server_socket and s != sock:
                                        s.sendall(msg)

                        else:
                            remove(sock, sockset, users)

                except:
                    remove(sock, sockset, users)


def get_next_word_packet(s, name):

    global packet_buffer

    length = int.from_bytes(packet_buffer[:2], 'big')

    while len(packet_buffer) < length + WORD_LEN_SIZE:

        packet_buffer += s.recv(5)

        length = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], 'big')

        if len(packet_buffer) == 0:

            return None

    word = packet_buffer[:length + WORD_LEN_SIZE]

    packet_buffer = packet_buffer[length + WORD_LEN_SIZE:]

    return word

def remove(sock, sockset, users=None):
    name = sock.getpeername()
    name = f"{name[0]}:{name[1]}"

    global server_socket

    if users:
        try:
            nick = users[name]
            del users[name]

            msg = {
                "type": "leave",
                "nick": nick
            }

            msg = json.dumps(msg, indent=0).encode()

            for s in sockset:
                if s != server_socket and s != sock:
                    s.sendall(msg)
        except KeyError:
            pass    

    
    print(f"*** {name}: disconnected")
    sock.close()
    sockset.remove(sock)
    
def usage():
    print("usage: chat_server.py port host", file=sys.stderr)
    
def main(argv):
    try:
        port = int(argv[1])
        if len(argv) > 2:
            host = argv[2]
        else:
            host = "localhost"
    except:
        usage()
        return 1
            
    
    run_server(host, port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
