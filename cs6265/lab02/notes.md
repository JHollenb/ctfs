# lab02 

## Login Information
```
OB3W4OLF1EIUVEMPGW26SFODHTKTIF2W
ssh lab02@52.201.10.159
b0258ba2

gdb-pwndbg ./target
br target.c:24
run < shellcode.bin
```
# Tut02
https://www.offensive-security.com/metasploit-unleashed/msfvenom/

Search for 
*exploit-db
*shell-storm.org
http://shell-storm.org/shellcode/

# 
```
gdb-pwndbg bomb
set follow-fork-mode parent
r /tmp/jakeholl-lab02/answers
b*0x00401295
b*0x00400d56
```

# env
Using ghidra, followed code execution and linked to variables:
```
global_var: 0x00602090
global_var_ro: 0x00400da8
print_key: 0x00400897
```

For the next var, using gdb, I stepped through the function and found the local path. Then I translated that to the actual environment.
```
local_var: 0x7fffffffe464 or 0x00007fffffffe4b4
```
gdb for local_var, we find what `0x4008970000012c` maps to, so `0x00007fffffffe460 + 0x4` in gdb and `0x00007fffffffe4b0 + 0x4` locally. 
```
 RAX  0x400897 (print_key) ◂— push   rbp
 RBX  0x0
 RCX  0x7ffff7b82cc0 (_nl_C_LC_CTYPE_class+256) ◂— add    al, byte ptr [rax]
 RDX  0x7fffffffe464 ◂— 0x4008970000012c

 RAX  0x7fffffffe464 ◂— 0xffffe4640000012c
 RBX  0x0
 RCX  0x10
 RDX  0x7fffffffe464 ◂— 0xffffe4640000012c

 > Here is your memory dump:
0x00007fffffffe440: 0x00007fffffffe470, p.......
0x00007fffffffe448: 0x0000000000400c70, p.@.....
0x00007fffffffe450: 0x00007fffffffe558, X.......
0x00007fffffffe458: 0x00000001004007b0, ..@.....
0x00007fffffffe460: 0x0000012cffffe550, P...,...
```

As for the PATH, again, gdb then guess until we get close to addr.

addr of PATH: 0x00007fffffffef4e

Once we get close, we can find beginning of PATH (/home) and calculate offset (0x00007fffffffef49 + 0x5)
```
> Which memory region do you want to see??
0x00007fffffffef49

> How many bytes?
100

> Here is your memory dump:
0x00007fffffffef49: 0x6f682f3d48544150, PATH=/ho
0x00007fffffffef51: 0x2f3a6e69622f656d, me/bin:/
0x00007fffffffef59: 0x61636f6c2f727375, usr/loca
0x00007fffffffef61: 0x2f3a6e6962732f6c, l/sbin:/
0x00007fffffffef69: 0x61636f6c2f727375, usr/loca
0x00007fffffffef71: 0x752f3a6e69622f6c, l/bin:/u
0x00007fffffffef79: 0x3a6e6962732f7273, sr/sbin:
0x00007fffffffef81: 0x6e69622f7273752f, /usr/bin
0x00007fffffffef89: 0x2f3a6e6962732f3a, :/sbin:/
0x00007fffffffef91: 0x7273752f3a6e6962, bin:/usr
0x00007fffffffef99: 0x2f3a73656d61672f, /games:/
0x00007fffffffefa1: 0x61636f6c2f727375, usr/loca
0x00007fffffffefa9: 0x0073656d61672f6c, l/games.
```
# References
* [Tutorial](https://tc.gts3.org/cs6265/2020-spring/tut/tut02-warmup2.html)
* [Assembly](https://www.cs.virginia.edu/~evans/cs216/guides/x86.html)
* [Session hijacking](https://en.wikipedia.org/wiki/Session_hijacking)

