#!/usr/bin/env python2

from pwn import *
from ctypes import *

def winnerWinner():
    val = libc.rand() % 3
    if val==0:
        retval = 1
    elif val==1:
        retval = 2
    elif val==2:
        retval = 0
    return retval

def intToVal(val):
    if val==0:
        return "rock"
    elif val==1:
        return "paper"
    elif val==2:
        return "scissors"

if __name__ == '__main__':
    libc = cdll.LoadLibrary("libc.so.6")

    # open a socket
    #s = remote("localhost", 9736)
    s = remote("52.201.10.159", 10700)

    # eat banner
    print s.recvline()

    name = "test"
    # send name
    s.send(name + "\n")
    libc.srand(u32(name) + libc.time(None))

    i = 1
    while i <= 6:
        # send my decision
        val = winnerWinner()
        s.send(intToVal(val) + "\n")

        # eat result
        result = s.recvline()
        print(result)

        # check result
        if "win" in result.lower():
            i += 1
            continue
        if "tie" in result.lower():
            continue
        else:
            #print s.recvall(timeout=5)
            s.interactive()
            exit(1)

    print s.recvall(timeout=5)

