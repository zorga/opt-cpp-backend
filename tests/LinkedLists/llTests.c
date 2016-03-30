#include <stdio.h>
#include <stdlib.h>

#include "thesis_LinkedList.h"

int main (int argc, char** argv)
{
	node_t* myList = init (18);
	push (&myList, 17);
	push (&myList, 16);
	printList (myList);
	free_list (&myList);
  return 0;
}

