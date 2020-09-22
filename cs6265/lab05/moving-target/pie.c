#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[])
{
  setreuid(geteuid(), geteuid());
  printf("%p\n", main);
  return 0;
}