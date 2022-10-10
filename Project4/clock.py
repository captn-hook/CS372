import socket
import sys
import datetime


def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(datetime.datetime.now().strftime("%s"))
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

#Saved Head
try:
    url = sys.argv[1]
except IndexError:
    url = "time.nist.gov"

try:
    port = int(sys.argv[2])
except IndexError:
    port = 37

try:
    retrys = int(sys.argv[3])
except IndexError:
    retrys = 10

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((url, port))

msg = b''

#Receive Response
for i in range(0, retrys):
    
    new = sock.recv(1024)
    msg += new

    if b'\r\n\r\n' in new or msg == 0:
        break

print(int.from_bytes(msg, 'big'))
print(system_seconds_since_1900())


#Close Socket
sock.close()
