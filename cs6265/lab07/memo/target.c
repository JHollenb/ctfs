#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include <linux/limits.h>
#include <openssl/md5.h>
#include <sys/stat.h>
#include <sys/types.h>

#define DB "/rw"
#define INPUT_SIZE 0x100
#define BUF_SIZE 0x1000

char name[INPUT_SIZE];
char udir[INPUT_SIZE];

void stripped_fgets(char* buf, size_t count, FILE* fp) {
  fgets(buf, count, fp);
  int len = strlen(buf);
  if (len > 0 && buf[len - 1] == '\n')
    buf[len - 1] = '\0';
}

void FATAL(const char* msg) {
  fprintf(stderr, "%s", msg);
  exit(-1);
}

char* md5str(char* str)  {
  unsigned char digest[16];
  char hexdigest[33];

  MD5_CTX ctx;
  MD5_Init(&ctx);
  MD5_Update(&ctx, str, strlen(str));
  MD5_Final(digest, &ctx);

  for (int i = 0; i < 16; i++)
    sprintf(&hexdigest[2 * i], "%02X", digest[i]);
  hexdigest[32] = 0;
  return strdup(hexdigest);
}

void join(const char* pass_file) {
  char pass[INPUT_SIZE] = "";

  // new name: create a new user directory
  printf("- Join: %s\n", name);
  printf("[*] Give me your new password\n");
  stripped_fgets(pass, sizeof(pass), stdin);
  char* hpass = md5str(pass);

  if (mkdir(udir, 0700) == -1)
    FATAL("[-] Failed to create a directory\n");

  FILE* fp = fopen(pass_file, "w");
  if (fp == NULL) {
    unlink(udir);
    FATAL("[-] Failed to make a password file\n");
  }

  fwrite(hpass, 1, 32, fp);
  
  printf("[+] Successfully joined\n");

  fclose(fp);
  free(hpass);

}

void login(FILE* fp) {
  char pass[INPUT_SIZE] = "";
  char buf[32] = "";

  printf("- Login: %s\n", name);
  
  if (fread(buf, 1, 32, fp) != 32) 
    FATAL("[-] Failed to read password\n");

  printf("[*] Give me your password\n");

  stripped_fgets(pass, sizeof(pass), stdin);
  char* hpass = md5str(pass);

  if (memcmp(buf, hpass, 32))
    FATAL("[-] Incorrect passwd\n");

  printf("[+] Successfully logged in\n");

  fclose(fp);
  free(hpass);
}

void write_memo() {
  char title[INPUT_SIZE] = "";
  char memo[INPUT_SIZE] = "";
  char size_s[INPUT_SIZE] = "";
  char buf[BUF_SIZE] = "";

  memset(buf, 0, sizeof(buf));

  printf("[*] Title?\n");
  stripped_fgets(title, sizeof(title), stdin);
  char* htitle = md5str(title);
  snprintf(memo, sizeof(memo), "%s/%s.txt", udir, htitle);

  if (access(memo, F_OK) != -1)
    FATAL("[-] Memo already exists\n");

  printf("[*] Size?\n");
  stripped_fgets(size_s, sizeof(size_s), stdin);
  int size = atoi(size_s);

  if (size <= 0 || size > BUF_SIZE)
    FATAL("[-] Invalid size\n");

  FILE* fp = fopen(memo, "wb");
  printf("[*] Data?\n");
  fread(buf, 1, size, stdin);
  fwrite(buf, 1, size, fp);

  free(htitle);
  fclose(fp);
}

void capitalize_read(char* memo, int size, int cap) {
  FILE* fp = fopen(memo, "rb");
  if (fp == NULL)
    FATAL("[-] Failed to open memo\n");

  int c = 0;
  char *buf = alloca(size);
  int read_bytes = 0;

  if (buf == NULL)
    FATAL("[-] Failed to allocate stack to read\n");

  while ((c = fgetc(fp)) != EOF) {
    if (cap)
      c = toupper(c);
    buf[read_bytes] = c;
    read_bytes++;
  }

  printf("[*] Data\n");
  fwrite(buf, 1, read_bytes, stdout);
  printf("\n");
  fclose(fp);
}

void read_memo() {
  char title[INPUT_SIZE] = "";
  char memo[INPUT_SIZE] = "";
  char cap[3];

  // get a memoy file
  printf("[*] Title?\n");
  stripped_fgets(title, sizeof(title), stdin);
  char* htitle = md5str(title);
  snprintf(memo, sizeof(memo), "%s/%s.txt", udir, htitle);

  // get a file size
  struct stat st;
  if (stat(memo, &st) == -1)
    FATAL("[-] Failed to get size of the memo\n");

  int size = st.st_size;

  printf("[*] Capitalize?\n");
  stripped_fgets(cap, sizeof(cap), stdin);

  capitalize_read(memo, size, cap[0] == 'y');
  
  free(htitle);
}

void remove_memo() {
  char title[INPUT_SIZE] = "";
  char memo[INPUT_SIZE] = "";

  // get a memoy file
  printf("[*] Title?\n");
  stripped_fgets(title, sizeof(title), stdin);
  char* htitle = md5str(title);
  snprintf(memo, sizeof(memo), "%s/%s.txt", udir, htitle);

  if (unlink(memo) == -1)
    FATAL("Failed to remove a memo\n");

  free(htitle);
}

void do_service() {
  char menu_s[3];

  while(1) {
    printf(
        "\n[*] Menu\n"
        "===============\n"
        "1. Write a memo\n"
        "2. Read a memo\n"
        "3. Remove a memo\n"
        "4. Exit\n");

    stripped_fgets(menu_s, sizeof(menu_s), stdin);
    int menu = atoi(menu_s);

    switch(menu) {
      case 1:
        write_memo();
        break;
      case 2:
        read_memo();
        break;
      case 3:
        remove_memo();
        break;
      case 4:
        printf("[*] Bye!\n");
        exit(0);
      default:
        printf("[-] No such command\n");
        break;
    }
  }
}

int main() 
{
  char pass_file[PATH_MAX] = "";

  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);

  printf("Welcome to the simple memo manager\n");

  // get user name
  printf("[*] Give me your name\n");
  stripped_fgets(name, sizeof(name), stdin);

  // set user directory
  char* hname = md5str(name);
  snprintf(udir, sizeof(udir), DB "/%s", hname);
  snprintf(pass_file, sizeof(pass_file), "%s/passwd.txt", udir);
  free(hname);

  // login or join
  FILE* fp = fopen(pass_file, "r");
  if (fp == NULL) {
    join(pass_file);
  }
  else 
    login(fp);

  do_service();
}
