#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *
import numpy as np

context.update(arch='i386')

io = remote('192.168.12.128', 2997)

num = []
for i in range (4):
    num.append(io.recv_raw(4))

uint_list = []
for data in num:
    uint_list.append(struct.unpack("i",data)[0])

send_val = 0
for data in uint_list:
    print('appending data', data)
    send_val = np.uintc(send_val + data)

print('Sending... ', send_val)
io.sendline(struct.pack("<I", send_val))
print(io.recvS())
