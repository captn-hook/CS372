from asyncio.windows_events import NULL
import socket
import sys

#Saved Head
try:
    url = sys.argv[1]
except IndexError:
    url = "example.com"

try:
    retrys = int(sys.argv[3])
except IndexError:
    retrys = 10

try:
    port = int(sys.argv[2])
except IndexError:
    port = 80

    
path = "/"

head = "GET " + path + " HTTP/1.1\r\nHost: " + url + "\r\nconnection: close\r\n\r\n"

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((url, port))

#Send Header
sock.sendall(head.encode("ISO-8859-1"))

#Receive Response
for i in range(0, retrys):
    
    msg = sock.recv(1024)

    if len(msg) == 0:
        break

    print(msg.decode("ISO-8859-1"))


#Close Socket
sock.close()