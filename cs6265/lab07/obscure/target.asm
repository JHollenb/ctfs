0001050c <main>:
   1050c:	e92d4800 	push	{fp, lr}
   10510:	e28db004 	add	fp, sp, #4
   10514:	e24ddc01 	sub	sp, sp, #256	; 0x100
   10518:	e3a0000a 	mov	r0, #10
   1051c:	ebffffa9 	bl	103c8 <alarm@plt>
   10520:	e59f305c 	ldr	r3, [pc, #92]	; 10584 <main+0x78>
   10524:	e5930000 	ldr	r0, [r3]
   10528:	e3a03000 	mov	r3, #0
   1052c:	e3a02002 	mov	r2, #2
   10530:	e3a01000 	mov	r1, #0
   10534:	ebffffaf 	bl	103f8 <setvbuf@plt>
   10538:	e59f3048 	ldr	r3, [pc, #72]	; 10588 <main+0x7c>
   1053c:	e5930000 	ldr	r0, [r3]
   10540:	e3a03000 	mov	r3, #0
   10544:	e3a02002 	mov	r2, #2
   10548:	e3a01000 	mov	r1, #0
   1054c:	ebffffa9 	bl	103f8 <setvbuf@plt>
   10550:	e59f0034 	ldr	r0, [pc, #52]	; 1058c <main+0x80>
   10554:	ebffff9e 	bl	103d4 <puts@plt>
   10558:	e3a0003e 	mov	r0, #62	; 0x3e
   1055c:	ebffffa8 	bl	10404 <putchar@plt>
   10560:	e24b3f41 	sub	r3, fp, #260	; 0x104
   10564:	e3a02c02 	mov	r2, #512	; 0x200
   10568:	e1a01003 	mov	r1, r3
   1056c:	e3a00000 	mov	r0, #0
   10570:	ebffff91 	bl	103bc <read@plt>
   10574:	e3a03000 	mov	r3, #0
   10578:	e1a00003 	mov	r0, r3
   1057c:	e24bd004 	sub	sp, fp, #4
   10580:	e8bd8800 	pop	{fp, pc}
   10584:	0002103c 	.word	0x0002103c
   10588:	00021038 	.word	0x00021038
   1058c:	00010600 	.word	0x00010600

