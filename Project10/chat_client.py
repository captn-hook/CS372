#python chat_client.py chris localhost 3490
import threading
import time
import sys
import socket
import json
import os

from chatui import init_windows, read_command, print_message, end_windows
#from chatuicurses import init_windows, read_command, print_message, end_windows
#chatui bug? if the message is longer than the screen width, it will get pushed into the cleared line
#if you do this more than once, the ghost lines will stack up
nick = None
s = None
maxsize = 1024

packet_buffer = b''

def usage():
    print("usage: chat_client.py nickname port host", file=sys.stderr)
    

def userin():
    global nick
    while True:
        try:
            command = read_command(f"{nick}> ")
        except:
            break
        
        if command != '' and command[0] == '/':
            #commands
            #/q quit
            if command == '/q':
                end_windows()
                os._exit(1)
                sys.exit(0)
                break
        
        print_message(f"{nick}: {command}")

        #make payload
        msg = {
            "type": "chat",
            "message": command
        }

        msg = packit(msg)
        
        #send the command to the server
        
        s.sendall(msg)

def packit(msg):
    
        msg = json.dumps(msg, indent=0)

        n = len(msg)

       
        newmsg = bytearray(n.to_bytes(2, 'big')) + msg.encode()
      
        return newmsg


def get_next_packet(s):

    global packet_buffer

    data = s.recv(maxsize)
 
    packet_buffer += data
    
    return slice_packet()

def slice_packet():

    global packet_buffer
    
    length = int.from_bytes(packet_buffer[:2], 'big')

    plen = len(packet_buffer) - 2

    if plen >= length:
  
        msg = packet_buffer[2:length+2].decode()
 
        packet_buffer = packet_buffer[length+2:]

        return msg

    else:
        return None

def main(argv):
    global nick
    global s
    try:
        nick = argv[1]
        port =int(argv[2])
        if len(argv) > 3:
            host = argv[3]
        else:
            host = "localhost"
    except:
        usage()
        return 1
            
    init_windows()

    s = socket.socket()


    # Make the client socket and connect
  

    try:
        s.connect((host, port))

        hellomsg = {
            "type": "hello",
            "nick": nick
        }

        hellomsg = packit(hellomsg)

        s.sendall(hellomsg)
            #s.sendall(hellomsg.encode())
            
    except:
        print_message("Unable to connect to server")
        end_windows()
        return 1

    
    t1 = threading.Thread(target=serverin, daemon=True)
    t1.start()

    userin()


def serverin():

    global s
    global nick

    while True:

        #recieve any response from the server
        
        try:
            data = get_next_packet(s)

            if data != None:
                data = json.loads(data)
                    
                if data["type"] == "chat" and data["nick"] != nick:
                    print_message(f"{data['nick']}: {data['message']}")

                elif data["type"] == "join":
                    print_message(f"*** {data['nick']} has joined the chat")

                elif data["type"] == "leave":
                    print_message(f"*** {data['nick']} has left the chat")

        except:
            print_message("Server has disconnected")
            end_windows()
            os._exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
