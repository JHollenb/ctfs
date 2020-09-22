#!/usr/bin/env python2

for i in range(0, 16):
    o1 = 0x56500000 | i << 16
    for j in range(0, 16):
        o2 = 0x56500000 | j << 12
        offset = o1 | o2
        print hex(offset)
