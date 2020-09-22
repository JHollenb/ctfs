#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#define MAX_NUM 3

char left;
struct note_t **notes;
unsigned long *sizes;
unsigned int total_cnt;

struct note_t
{
	char title[64];
	char body[0];
};

void welcome()
{
	puts("Welcome to CS6265 cloud note database");
}

int menu()
{
	unsigned int choice;

	puts("====================");
	puts("1) Add a note");
	puts("2) Delete a note");
	puts("3) Edit a note");
	puts("4) Print all notes");
	puts("5) Print a note");
	puts("6) Exit");
	puts("====================");

	printf("$ ");
	scanf("%u%c", &choice, &left);
	
	if (choice <= 6 && choice >= 1)
		return choice;
	else
		return -1;
}

void add()
{
	unsigned long size = 0;
	int i;
	struct note_t *note;
	char buf[0x18];
	
	if (total_cnt == MAX_NUM)
	{
		puts("There is no space.");
		return;
	}

	printf("Input length of your new note: ");
	fgets(buf, 16, stdin);
	size = strtoll(buf, 0, 10);
	note = (struct note_t *)malloc(size + 64);

	printf("Input note title (at most 63 bytes): ");
	fgets(note->title, 63, stdin);

	printf("Input note body (at most %ld bytes): ", size);
	fgets(note->body, size, stdin);

	for (i = 0; i < MAX_NUM && notes[i]; i++);

	notes[i] = note;
	sizes[i] = size + 64;
	total_cnt++;

	return;
}

void delete()
{
	unsigned int index;

	printf("Which note do you want to delete: ");
	scanf("%u%c", &index, &left);

	if (index < MAX_NUM)
	{
		if (notes[index])
		{
			free(notes[index]);
			notes[index] = NULL;
			sizes[index] = 0;
			total_cnt--;
		}
	}
	else
	{
		puts("Wrong index");
	}

	return;
}

void edit()
{
	unsigned int index;
	unsigned int choice;
	
	printf("Which note do you want to edit: ");
	scanf("%u%c", &index, &left);

	if (index < MAX_NUM)
	{
		if (notes[index])
		{
			choice = -1;
			do
			{
				printf("1) Edit title\n2) Edit body\n$ ");
				scanf("%u%c", &choice, &left);
			} while (choice != 1 && choice != 2);

			if (choice == 1)
			{
				printf("Input new note title: ");
				fgets(notes[index]->title, 63, stdin);
			}
			else
			{
				printf("Input new note body: ");
				fgets(notes[index]->body, sizes[index], stdin);
			}
		}
		else
		{
			puts("Wrong index");
		}
	}
	else
		puts("Wrong index");
	
	return;
}

void print_all()
{
	int i = 0;
	for (; i < MAX_NUM; i++)
	{
		if (notes[i])
		{
			printf("===== No. %d =====\n", i);
			printf("Title: %s\n", notes[i]->title);
			printf("Content: %s\n", notes[i]->body);
		}
	}

	return;
}

void print()
{
	unsigned int index;
	
	printf("Which note do you want to view: ");
	scanf("%u%c", &index, &left);

	if (notes[index])
	{
		printf("===== No. %d =====\n", index);
		printf("Title: %s\n", notes[index]->title);
		printf("Content: %s\n", notes[index]->body);
	}
	else
	{
		puts("Wrong index");
	}

	return;
}

int main()
{
	setreuid(geteuid(), geteuid());

	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 2, 0);
	welcome();

	notes = (struct note_t **)malloc(MAX_NUM * 0x8);
	memset(notes, 0, MAX_NUM * 0x8);
	sizes = (unsigned long *)malloc(MAX_NUM * 0x8);
	memset(sizes, 0, MAX_NUM * 0x8);
	total_cnt = 0;

	while (1)
	{
		switch ( menu() )
		{
			case 1:
				add();
				break;

			case 2:
				delete();
				break;

			case 3:
				edit();
				break;

			case 4:
				print_all();
				break;

			case 5:
				print();
				break;

			case 6:
				exit(0);

			default:
				puts("Invalid option");
				break;
		}
	}

	return 0;
}


