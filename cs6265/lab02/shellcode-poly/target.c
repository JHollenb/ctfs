#include <stdio.h>
#include <string.h>
#include <err.h>
#include <seccomp.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <limits.h>

#define SECRET_FILE "./secret.bin"
#define SECRET_SIZE 64

char secret[SECRET_SIZE];
char chars[] = {'a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

void print_key() {
  char buf[1024];
  FILE *fp = fopen("/proc/flag", "r+");
  if (!fp)
    err(1, "Please insert your kflag.ko to get the flag!");
  printf("This is your flag:\n\n");
  while (1) {
    size_t len = fread(buf, 1, sizeof(buf)-1, fp);
    buf[len] = '\0';
    printf("%s", buf);
    if (len < sizeof(buf)-1)
      break;
  }
  printf("\n");
  fclose(fp);
}

void initialize_secret() {
  FILE* fp = fopen("/dev/urandom", "rb");
  char ch;
  if (fp == NULL)
    err(1, "failed to open /dev/urandom");

  for (int i = 0; i < SECRET_SIZE; i++) {
    fread(&ch, 1, 1, fp);
    secret[i] = chars[ch % sizeof(chars)];
  }
  fclose(fp);

  fp = fopen(SECRET_FILE, "wb");
  if (fp == NULL)
    err(1, "failed to open %s", SECRET_FILE);
  fwrite(secret, 1, sizeof(secret), fp);
  fclose(fp);
}

void run_target(char* target, char* buf, size_t buflen,
                char* out, size_t outlen) {
  int ifd[2], ofd[2];
  int status;
  pid_t pid;

  pipe(ifd);
  pipe(ofd);

  if ((pid = fork()) == -1)
    err(1, "fork");

  if (pid == 0)
  {
    /* Child process closes up input side of pipe */
    close(ifd[1]);
    close(ofd[0]);
    dup2(ifd[0], 0);
    dup2(ofd[1], 1);
    execl(target, target, NULL);
    exit(0);
  }
  else
  {
    close(ifd[0]);
    close(ofd[1]);

    write(ifd[1], buf, buflen);
    read(ofd[0], out, outlen);
    wait(&status);

    close(ifd[0]);
    close(ofd[1]);
  }
}

void get_base_dir(char* path) {
  ssize_t bytes = readlink("/proc/self/exe", path, PATH_MAX);
  if (bytes < 0)
    err(1, "cannot get a base directory");
  char* p = strrchr(path, '/');
  if (p == NULL)
    err(1, "cannot find '/'");
  *(p+1) = '\0';
}

int main(int argc, char *argv[])
{
  char buf[2048];
  char out[SECRET_SIZE];
  initialize_secret();

  printf("Give me a shellcode reading 'secret.bin' in both 32 & 64 bit\n");
  if (!fgets(buf, sizeof(buf), stdin))
    err(1, "Too long input");

  char *targets[] = {"target32", "target64"};
  for (int i = 0; i < 2; i ++) {
    char path[PATH_MAX];
    get_base_dir(path);
    strncat(path, targets[i], sizeof(path) - strlen(path) - 1);
    memset(out, 0, sizeof(out));
    run_target(path, buf, sizeof(buf), out, sizeof(out));
    if (memcmp(out, secret, sizeof(out))) {
      printf("No, your shellcode is wrong\n");
      exit(-1);
    }
  }

  printf("Well done!\n");
  print_key();

  return 0;
}