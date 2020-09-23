#include <sys/syscall.h>

.intel_syntax noprefix

.globl main
.type  main, @function

main:
  xor    rdi,rdi                /* arg 1: 0 */
  mov    rax, rdi
  mov    al, SYS_exit           /* #syscall */
  syscall                       /* exit(0) */
