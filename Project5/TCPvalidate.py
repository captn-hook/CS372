import sys
import os
from typing import ByteString

#if argument, use as path, else use default
if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    path = "tcp_data"

files = os.listdir(path)

#seperate files into two lists by name, one for data and one for addrs
data = []
addrs = []

for i in files:
    if i[0:9] == "tcp_data_":
        data.append(i)
    elif i[0:10] == "tcp_addrs_":
        addrs.append(i)

def IPbytes(ip):
    #converts IP address to bytes
    ip = ip.rstrip().split(".")

    bites = b''

    for i in ip:
        bites += int(i).to_bytes(1, 'big')

    return bites

for i in range(len(data)):
    #open addr and split
    addr_file = open(path + "/" + addrs[i], "r")

    address = addr_file.read().split(" ")

    addr_file.close()

    address[0] = IPbytes(address[0])
    address[1] = IPbytes(address[1])

    #open data and decode
    data_file = open(path + "/" + data[i], "rb")

    file = data_file.read()

    length = len(file)

    data_file.close()

    #check if length is correct
    pseudo = address[0] + address[1] + b'\x00' + b'\x06' + length.to_bytes(2, 'big')

    check = int.from_bytes(file[16:18], 'big')

    zeroCheck = file[:16] + b'\x00\x00' + file[18:]

    if len(zeroCheck) % 2 == 1:
        zeroCheck += b'\x00'

    packet = pseudo + zeroCheck

    offset = 0

    total = 0

    while offset < len(packet):
    # Slice 2 bytes out and get their value:

        word = int.from_bytes(packet[offset:offset + 2], 'big')

        total += word

        total = (total & 0xffff) + (total >> 16)

        offset += 2   # Go to the next 2-byte value

    total = (~total) & 0xffff

    if total == check:
        print("PASS")
    else:
        print("FAIL")
