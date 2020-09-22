#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

#define MAX_SIZE 0x10000

typedef struct _node {
  struct _node* next;
  char data[0];
} node;

node* head = NULL;
uint32_t read_int() {
  char buf[10];
  ssize_t size = read(0, buf, sizeof(buf) - 1);
  buf[size] = '\0';
  uint32_t res = atoi(buf);
  return res;
}

void read_with_null(int fd, char* buf, size_t size) {
  ssize_t read_bytes = read(0, buf, size);
  if (buf[read_bytes - 1] == '\n')
    buf[read_bytes - 1] = '\0';
  else
    buf[read_bytes] = '\0';
}

void add() {
  printf("Size?\n");
  uint32_t size = read_int();

  if (size > MAX_SIZE) {
    printf("Too large size\n");
    exit(-1);
  }

  node* new = (node*)malloc(sizeof(node) + size);
  if (new == NULL) {
    printf("Error : Out of memory\n");
    return;
  }
  new->next = NULL;

  printf("Data?\n");
  read_with_null(0, new->data, size);

  if (head == NULL)
    head = new;
  else {
    node *ptr = head;
    while (ptr->next != NULL)
      ptr = ptr->next;
    ptr->next = new;
  }
  printf("Success\n");
}

void print() {
  node* ptr = head;
  uint32_t i = 0;
  printf("Print all nodes\n\n");
  while(ptr != NULL) {
    printf("Node(%d): %s\n", i, ptr->data);
    ptr = ptr->next;
    i++;
  }
}

void delete() {
  if (head == NULL) {
    printf("Error : Nothing to delete\n");
    return;
  }

  printf("Index to delete?\n");
  uint32_t index = read_int();
  node *ptr = head, *prev;

  if (index == 0) {
    // delete head
    head = ptr->next;
    free(ptr);
    printf("Success : Remove head\n");
    return;
  }

  for (int i = 0; i < index && ptr; i++) {
    prev = ptr;
    ptr = ptr->next;
  }

  if (ptr == NULL) {
    printf("Error : Invalid index\n");
    return;
  }

  prev->next = ptr->next;
  free(ptr);
  printf("Success : Remove %dth entry\n", index);
}

void change() {
  if (head == NULL) {
    printf("Error : Nothing to change\n");
    return;
  }

  printf("Index to change?\n");
  uint32_t index = read_int();
  node *ptr = head;

  for (uint32_t i = 0; i < index && ptr; i++) {
    ptr = ptr->next;
  }

  if (ptr == NULL) {
    printf("Error : Invalid index\n");
    return;
  }

  printf("Size?\n");
  int size = read_int();

  printf("Data?\n");
  read_with_null(0, ptr->data, size);

  printf("Success : Change %dth entry\n", index);
}

int main() {
  setreuid(geteuid(), geteuid());
  setvbuf(stdin ,NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);

  printf("Welcome to Linked list\n");

  while(true) {
    printf("\n1. Add\n2. Delete\n3. Change\n4. Print\n5. Exit\n");
    switch(read_int()) {
      case 1:
        add();
        break;
      case 2:
        delete();
        break;
      case 3:
        change();
        break;
      case 4:
        print();
        break;
      case 5:
        exit(0);
    }
  }
}
