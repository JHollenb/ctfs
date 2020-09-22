# ctfs

# RE
## `checksec`

```
siuser@ubuntu:~/repos/ctfs/fusion/level03$ ./exploit.py 
[*] '/home/siuser/repos/ctfs/fusion/level03/level03'
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
    RPATH:    '/opt/fusion/lib'
    FORTIFY:  Enabled
```

NX - Used to indicate if the stack is executable or not. This means can't inject. Need ROP.
PIE - Position Independent. We will neeed a leak.

# ROPGadget

## Installation
```
pip install ROPGadget
```

## Searching for systems calls

```
fusion@fusion:/opt/fusion/bin$ readelf -s /lib/i386-linux-gnu/libc.so.6 | egrep " system| exit"                                                                                      
   135: 000329e0    45 FUNC    GLOBAL DEFAULT   12 exit@@GLIBC_2.0
  1409: 0003cb20   139 FUNC    WEAK   DEFAULT   12 system@@GLIBC_2.0
fusion@fusion:/opt/fusion/bin$ 
```

## Searching for `puts` in GOT and PLT

```
fusion@fusion:/opt/fusion/bin$ objdump -d ./level02 | grep -A1 puts
08048930 <puts@plt>:
 8048930:       ff 25 b8 b3 04 08       jmp    *0x804b3b8
--
 8049807:       e8 24 f1 ff ff          call   8048930 <puts@plt>
 804980c:       c7 45 f4 01 00 00 00    movl   $0x1,-0xc(%ebp)
--
 80498b0:       e8 7b f0 ff ff          call   8048930 <puts@plt>
 80498b5:       c7 44 24 08 04 00 00    movl   $0x4,0x8(%esp)
fusion@fusion:/opt/fusion/bin$ 
```

```
puts@plt = 0x08048930 
puts@got = 0x0804b3b8
```

## Searching for `"bin/sh"` offset
```
fusion@fusion ~ $ strings -atx /lib/i386-linux-gnu/libc.so.6 | grep "/bin/sh"
```

# GDB
## Following a remote process:
```
$ ps -aux | grep level02
Warning: bad ps syntax, perhaps a bogus '-'? See http://procps.sf.net/faq.html
20002     3181  0.0  0.0   1816   340 ?        Ss   Sep12   0:00 /opt/fusion/bin/level02
root     13690  0.0  0.0   4496  1172 pts/0    S+   01:31   0:00 sudo gdb ./level02
root     13691  0.0  0.7  26408 16212 pts/0    S+   01:31   0:00 gdb ./level02
fusion   14003  0.0  0.0   4184   796 pts/1    S+   01:59   0:00 grep --color=auto level02
```

```
(gdb) attach 3181
(gdb) set follow-fork-mode child
(gdb) c
```

## Finding address
### GDB
```
(gdb) p system
$1 = {<text variable, no debug info>} 0xb767fb20 <__libc_system>
 
(gdb) p exit
$2 = {<text variable, no debug info>} 0xb76759e0 <__GI_exit>
 
(gdb) find 0xb767fb20, +9999999, "/bin/sh"
0xb777b8da
warning: Unable to access target memory at 0xb77bdf62, halting search.
1 pattern found.
```

### objdump
```
andrew ~/fusion/level03 $ objdump -d level03 | grep -A1 "__libc_start_main@plt>:"
08048d80 <__libc_start_main@plt>:
 8048d80:       ff 25 2c bd 04 08       jmp    *0x804bd2c
```

### rabin2
```
andrew ~/fusion/level03 $ rabin2 -s level03 | egrep 'memcpy|post_blog_article|gTitle$'
100  0x00001f20 0x08049f20 GLOBAL FUNC   745      post_blog_article
132  ---------- 0x0804be04 GLOBAL OBJ    4        gTitle
39   0x00000e60 0x08048e60 GLOBAL FUNC   16       imp.memcpy
```

# Global Variable addresses
```
$ nm crackme0x00 | grep secret
0804a050 D secret
```

# Ret2Lib
## x86
For the following calls:
```
  open("/proc/flag", O_RDONLY)
  read(3, tmp, 1024)
  write(1, tmp, 1024)
```
This is how we want the program to look:
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
  [arg3     ] -> 1024
```


# References
## Binary Exploitation
[John Hammond: ROP](https://www.youtube.com/watch?v=i5-cWI_HV8o&pbjreload=101)
