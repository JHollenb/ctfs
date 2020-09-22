#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

void start(char *src) {
  char buf[10];
  strncpy(buf, src, 30);
  return;
}

int main(int argc, char *argv[]) {
  setreuid(geteuid(), geteuid());
  if (argc < 2) {
    exit(-1);
  }
  start(argv[1]);
}
