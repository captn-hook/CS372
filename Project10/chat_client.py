#python chat_client.py chris localhost 3490
import threading
import time
import sys
import socket

from chatui import init_windows, read_command, print_message, end_windows
#from chatuicurses import init_windows, read_command, print_message, end_windows


def usage():
    print("usage: chat_client.py nickname host port", file=sys.stderr)
    

def runner():
    count = 0

    while True:
        time.sleep(2)
        print_message(f"*** Runner count: {count}")
        count += 1

def main(argv):
    try:
        nick = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1
            
    init_windows()

    t1 = threading.Thread(target=runner, daemon=True)
    t1.start()

    # Make the client socket and connect
    s = socket.socket()

    try:
        s.connect((host, port))
    except:
        print_message("Unable to connect to server")
        return 1

    while True:
        try:
            command = read_command("Enter a thing> ")
        except:
            break
        
        if command[0] == '/':
            #commands
            #/q quit
            if command == '/q':
                break
        else:
            print_message(f"{nick}> {command}")

    end_windows()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
