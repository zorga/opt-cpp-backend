#include <stdio.h>
#include <stdlib.h>

#include "thesis_LinkedList.h"

int main (int argc, char** argv)
{
	node_t* head = init (18);
	push (&head, 17);
	free_list (&head);
  return 0;
}

