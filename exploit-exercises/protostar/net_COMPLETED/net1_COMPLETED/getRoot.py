#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

context.update(arch='i386')

io = remote('192.168.12.128', 2998)
line = io.recvS()
print(line)
num = u32(line)
print(num)
io.send(str(num))
print(io.recv())
