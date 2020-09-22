#include <sys/syscall.h>

.intel_syntax noprefix

.globl main
.type  main, @function

main:
  xor    ebx,ebx
  mov    eax,ebx
  inc    eax
  int    0x80
