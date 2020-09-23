#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

struct note_t
{
	char content[25];
	char name[27];
	struct note_t *next;
};

struct control_t
{
	unsigned int pub_cnt;
	unsigned int new_cnt;
	struct note_t *head;
	char *msg_ptr;	
};

char msg_content[128];

struct control_t control;

void _enter(char *buf)
{
	int len = strlen(buf) - 1;

	if ( len >= 0 && buf[len] == '\n')
		buf[len] = 0;
}

int menu_choice()
{
	unsigned int choice;
	char s[32];

	do
	{
		printf("> ");
		fgets(s, 32, stdin);
	} while ( !sscanf(s, "%u", &choice) );

	return choice;
}

void add()
{
	struct note_t *p = control.head;
	control.head = malloc(56);
	
	if (control.head)
	{
		(control.head)->next = p;
		printf("Note title: ");
		fgets((control.head)->name, 56, stdin);
		_enter((control.head)->name);

		printf("Note content: ");
		fgets((control.head)->content, 56, stdin);
		_enter((control.head)->content);

		control.new_cnt++;
	}
	else
	{
		puts("Something wrong!");
	}
	
	return;
}

void show()
{
	struct note_t *p = control.head;
	printf("Here are the notes to be published:\n");
	puts("=====================================");

	for (; p ; p = p->next)
	{
		printf("Note: %s\n", p->name);
		printf("Content: %s\n", p->content);
		puts("=====================================");
	}

	return;
}

void publish()
{
	struct note_t *p = control.head, *q;

	if (control.new_cnt)
	{
		while (p)
		{
			q = p;
			p = p->next;
			free(q);
		}

		control.head = NULL;
		control.pub_cnt++;
		puts("All notes published!");
	}
	else
	{
		puts("No notes are waiting to be published!");
	}

	return;
}

void leave()
{
	puts("Enter your secret note!");
	fgets(control.msg_ptr, 128, stdin);
	_enter(control.msg_ptr);

	return;
}

void history()
{
	puts("===== History =====");
	printf("Total: %u notes\n", control.new_cnt);
	printf("Publish: %u times\n", control.pub_cnt);

	if (control.msg_ptr)
		printf("Secret: %s\n", control.msg_ptr);
	
	return;
}

void menu()
{
	puts("===== Command List =====");
	puts("1. Add new note");
	puts("2. Show all notes");
	puts("3. Publish all notes");
	puts("4. Leave a secret note");
	puts("5. Show history");
	puts("6. Exit");

	while (1)
	{
		switch (menu_choice())
		{
			case 1:
				add();
				break;
			case 2:
				show();
				break;
			case 3:
				publish();
				break;
			case 4:
				leave();
				break;
			case 5:
				history();
				break;
			case 6:
				puts("bye");
				return;
			default:
				break;
		}
	}

	return;
}

int main()
{
	setreuid(geteuid(), geteuid());
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);

	control.pub_cnt = 0;
	control.new_cnt = 0;
	control.msg_ptr = msg_content;
	control.head = NULL;

	puts("Welcome to Note Center!");
	menu();

	return 0;
}


		
