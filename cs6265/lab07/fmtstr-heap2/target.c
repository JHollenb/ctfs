#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <common.h>

#define SIZE 0x1000

int main(int argc, char** argv) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);

  char *buf = malloc(SIZE + 1);

  while(1) {
    printf("Give me something...\n");  
    fgets(buf, SIZE + 1, stdin);
    if (!strncmp(buf, "exit", 4))
      break;

    printf(buf);
  }
  printf("Bye\n");
  free(buf);
}
