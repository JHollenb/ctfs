#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <common.h>

void jump_to_here() {
  read_flag();
}

void start() {
  char buffer[50];
  printf("Please input something...\n");
  fgets(buffer, 512, stdin);
}

int main(int argc, char** argv) {
  setreuid(geteuid(), geteuid());
  /* no warning */
  (void)jump_to_here;
  start();
  return 0;
}
