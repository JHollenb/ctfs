#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

/*
 * please add -static and -L<lib64 path> when distributing
 * libc <= 2.23 is recommended (because of _IO_vtable_check())
 *
 * or you can use Makefile provided (recommended)
 */

typedef struct {
  char buf[0x100];
  FILE* fp;
} my_struct;

int main() {
  setreuid(geteuid(), geteuid());
  my_struct st;
  st.fp = stdout;
  fgets(st.buf, 0x200, stdin);
  fputs(st.buf, st.fp);
}
