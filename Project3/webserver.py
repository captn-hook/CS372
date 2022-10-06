from copyreg import constructor
import socket
import sys

try:
    port = int(sys.argv[1])
except IndexError:
    port = 28333

#Saved Response
def buildPayload(f):
    payload = f.read()
    Clen = len(payload.encode("ISO-8859-1"))
    return payload, Clen

def buildResponse(request):

    if request == '' or request == '/' or request == '/index.html':
        with open('index.html', 'r') as f:
            print("index.html")
            Ctype = "text/html"
            payload, Clen = buildPayload(f)
            
    elif request == '/file.txt':
        with open('file.txt', 'r') as f:
            print("file.txt")
            Ctype = "text/plain"
            payload, Clen = buildPayload(f)
    elif request == '/index.js':
        with open('index.js', 'r') as f:
            print("index.js")
            Ctype = "text/javascript"
            payload, Clen = buildPayload(f)
    else:
        with open('missing.html', 'r') as f:
            print("missing.html")
            Ctype = "text/html"
            payload, Clen = buildPayload(f)

    response = "HTTP/1.1 200 OK\r\nContent-Type: " + Ctype + "\r\nContent-Length: " + str(Clen) + "\r\nConnection: close\r\n\r\n" + payload
    return response

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("127.0.0.1", port))

sock.listen()

while True:
    
    connect, addr = sock.accept()

    msg = ''

    print(connect)

    while True:

        msg += connect.recv(2).decode("ISO-8859-1")


        if "\r\n\r\n" in msg:
            break

    i = msg.find('HTTP')

    c = 0

    for slash in msg[4:i - 1]:
        if slash == '/':    
            c += 1

    if c > 1:
        response = buildResponse('')
    else:
        response = buildResponse(msg[4:i - 1])

    connect.sendall(response.encode("ISO-8859-1"))

    connect.close()
    