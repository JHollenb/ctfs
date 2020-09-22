#!/usr/bin/env python2

import os
import re
import sys

from pwn import *

context.arch = "x86"
context.bits = 32
exe = "./crackme0x00"

# Assume a process or remote connection
p = process(exe)
e = ELF(exe)

# Declare a function that takes a single address, and
# leaks at least one byte at that address.
def leak(address):
    data = p.read(address, 4)
    log.debug("%#x => %s" % (address, enhex(data or '')))
    return data

# For the sake of this example, let's say that we
# have any of these pointers.  One is a pointer into
# the target binary, the other two are pointers into libc
main   = 0x0804885e
libc   = 0xdeadb000
system = 0xdeadbeef

# With our leaker, and a pointer into our target binary,
# we can resolve the address of anything.
# However, if we *do* have a copy of the target binary,
# we can speed up some of the steps.
d = DynELF(leak, main, elf=e)
assert d.lookup(None,     'libc') == libc
assert d.lookup('system', 'libc') == system


print d.stack()
# Alternately, we can resolve symbols inside another library,
# given a pointer into it.
#d = DynELF(leak, libc + 0x1234)
#assert d.lookup('system')      == system
