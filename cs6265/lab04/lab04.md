# Overview
```
ssh lab04@52.201.10.159
72cb6693

scp -r lab04@52.201.10.159:~ .
```


```
0x0804860b in main ()
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
────────────────────────────────────────────[ REGISTERS ]─────────────────────────────────────────────
 EAX  0xffffd67b ◂— 0x66666666 ('ffff')
 EBX  0x5a29
 ECX  0x5a29
 EDX  0x0
 EDI  0x0
 ESI  0xf7fbd000 (_GLOBAL_OFFSET_TABLE_) ◂— insb   byte ptr es:[edi], dx /* 0x1d7d6c */
 EBP  0xffffd478 ◂— 0x0
 ESP  0xffffd470 —▸ 0xffffd67b ◂— 0x66666666 ('ffff')
 EIP  0x804860b (main+67) —▸ 0xffff66e8 ◂— 0x0
──────────────────────────────────────────────[ DISASM ]──────────────────────────────────────────────
   0x80485e6 <main+30>    jg     main+58 <0x8048602>
    ↓
   0x8048602 <main+58>    mov    eax, dword ptr [ebp + 0xc]
   0x8048605 <main+61>    add    eax, 4
   0x8048608 <main+64>    mov    eax, dword ptr [eax]
   0x804860a <main+66>    push   eax
 ► 0x804860b <main+67>    call   start <0x8048576>
        arg[0]: 0xffffd67b ◂— 0x66666666 ('ffff')
        arg[1]: 0x0
        arg[2]: 0x0
        arg[3]: 0xf7dfde81 (__libc_start_main+241) ◂— add    esp, 0x10

   0x8048610 <main+72>    add    esp, 4
   0x8048613 <main+75>    mov    eax, 0
   0x8048618 <main+80>    mov    ebx, dword ptr [ebp - 4]
   0x804861b <main+83>    leave
   0x804861c <main+84>    ret
──────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────
00:0000│ esp  0xffffd470 —▸ 0xffffd67b ◂— 0x66666666 ('ffff')
01:0004│      0xffffd474 ◂— 0x0
... ↓
03:000c│      0xffffd47c —▸ 0xf7dfde81 (__libc_start_main+241) ◂— add    esp, 0x10
04:0010│      0xffffd480 ◂— 0x2
05:0014│      0xffffd484 —▸ 0xffffd514 —▸ 0xffffd65c ◂— 0x6d6f682f ('/hom')
06:0018│      0xffffd488 —▸ 0xffffd520 —▸ 0xffffd7a4 ◂— 0x435f534c ('LS_C')
07:001c│      0xffffd48c —▸ 0xffffd4a4 ◂— 0x0
────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────
 ► f 0  804860b main+67
   f 1 f7dfde81 __libc_start_main+241
pwndbg> x/20wx $esp
0xffffd470:     0xffffd67b      0x00000000      0x00000000      0xf7dfde81
0xffffd480:     0x00000002      0xffffd514      0xffffd520      0xffffd4a4
0xffffd490:     0x00000001      0x00000000      0xf7fbd000      0xf7fe575a
0xffffd4a0:     0xf7ffd000      0x00000000      0xf7fbd000      0x00000000
0xffffd4b0:     0x00000000      0x0cc6776c      0x4cd3f17c      0x00000000
pwndbg>
```

0x5e4cb4e4
0x5e4cb523 -> 0x5e693672
0x5e4cb55d -> 0x2d6eb1c
