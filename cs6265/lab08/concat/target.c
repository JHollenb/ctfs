#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <err.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define NAME_LEN 0x1000
#define BUF_LEN 0x100

void read_flag() {
  char buf[2048];
  int fd = open("/proc/flag", 0);
  if (fd == -1)
    return;
  memset(buf, 0, sizeof(buf));
  ssize_t size = read(fd, buf, sizeof(buf));
  if (size != -1)
  write(1, buf, size);
  close(fd);
}

void fgets_strip(char* buf, size_t count, FILE* fp) {
  fgets(buf, count, fp);
  int len = strlen(buf);
  if (len >= 0 && buf[len -1] == '\n')
    buf[len - 1] = '\0';
}

void hello() {
  char name[NAME_LEN];
  memset(name, 0, sizeof(name));
  printf("What's your name?\n");
  fgets_strip(name, sizeof(name), stdin);
  printf("Hello %s\n", name);
}

void concat() {
  char out[BUF_LEN * 2 + 1];
  char buf1[BUF_LEN];
  char buf2[BUF_LEN];

  printf("Give me 1st input\n");
  fgets_strip(buf1, sizeof(buf1), stdin);
  printf("Give me 2nd input\n");
  fgets_strip(buf2, sizeof(buf2), stdin);

  strcpy(out, buf1);
  strcat(out, buf2);
  printf("Concatenated: %s\n", out);
}

int main() {
  setreuid(geteuid(), geteuid());
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);

  hello();
  concat();
}
