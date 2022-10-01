from copyreg import constructor
import socket
import sys

try:
    port = int(sys.argv[1])
except IndexError:
    port = 28333

#Saved Response

Ctype = "text/plain"
payload = ""
Clen = len(payload)
response = "HTTP/1.1 200 OK\r\nContent-Type: " + Ctype + "\r\nContent-Length: " + str(Clen) + "\r\nConnection: close\r\n\r\n" + payload

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("127.0.0.1", port))

sock.listen()

while True:
    print("Waiting for connection...")
    connect, addr = sock.accept()

    print(connect)
    while True:

        msg = connect.recv(4096).decode("ISO-8859-1")


        if "\r\n\r\n" in msg:
            break

    print(msg)

    connect.sendall(response.encode("ISO-8859-1"))

    connect.close()