# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select
import json

server_socket = None

packet_buffer = {}

maxsize = 1024


def packit(msg):
    
        msg = json.dumps(msg, indent=0)

        n = len(msg)
       
        newmsg = bytearray(n.to_bytes(2, 'big')) + msg.encode()
      
        return newmsg

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
                    
                    name = sock.getpeername()

                    name = f"{name[0]}:{name[1]}"

                    data = get_next_packet(sock, name)                    

                    if data != None and data != b'' and data != '':

                        data =  json.loads(data)

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
                                        s.sendall(packit(msg))

                            

                        elif users[name]:

                            nick = users[name]                   

                            print(f"{name}: {nick}> {data['message']}")

                            msg = {
                                "type": "chat",
                                "nick": nick,
                                "message": data["message"]
                            }

                            for s in sockset:
                                if s != server_socket and s != sock:
                                    s.sendall(packit(msg))

                except Exception as e:
                    remove(sock, sockset, users)


def get_next_packet(s, name):

    global packet_buffer

    data = s.recv(maxsize)

    if name in packet_buffer:
        packet_buffer[name] += data
        return slice_packet(name, packet_buffer)
        

    else:
        packet_buffer[name] = data
        return slice_packet(name, packet_buffer)     

def slice_packet(name, packet_buffer):

    length = int.from_bytes(packet_buffer[name][:2], 'big')
    plen = len(packet_buffer[name]) - 2

    if plen >= length:
  
        msg = packet_buffer[name][2:length+2].decode()
 
        packet_buffer[name] = packet_buffer[name][length+2:]

        return msg
    else:
        print(f"*** {name}: {plen} bytes: incomplete")
        return None


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

            for s in sockset:
                if s != server_socket and s != sock:
                    s.sendall(packit(msg))
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
    except Exception as e:
        print(e)
        usage()
        return 1
            
    
    run_server(host, port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
