#include <stdio.h>
#include <stdlib.h>
#include "thesis_LinkedList.h"

#define PRINT_ADDR_PTR

int main (int argc, char** argv)
{
  node_t* head = buildOneTwoThree ();
  free_list (&head);
  return 0;
}

int length (node_t* head)
{
  int len = 0;
  node_t* curr = head;
  while (curr->next)
  {
    len++;
    curr = curr->next;
  }
  return len;
}

void push (node_t** headRef, int newData)
{
  node_t* newHead = (node_t*) malloc (sizeof (node_t)); 
  newHead->data = newData;
  newHead->next = *headRef;
  *headRef = newHead; // changing a Pointer using a Reference Pointer (Pointer to Pointer)
}

node_t* init (int initData)
{
  node_t* head = (node_t*) malloc (sizeof (node_t));
  head->next = NULL;
  head->data = initData;
  return head;
}

node_t* buildOneTwoThree ()
{
  node_t* head = init (0);
  push(&head, 1);
  push(&head, 2);
  push(&head, 3);
  return head;
}

void printList (node_t* head)
{
  int count = 0;
  node_t* current = head;
  for (current = head; current != NULL; current = current->next)
  {
    printf ("%d\n", current->data);
    count++;
  }
  printf ("Length of the list : %d\n", count);
}

node_t* buildWithLocalRef ()
{
  node_t* head = NULL;
  node_t** lastPtrRef = &head; // Start out pointing to the head pointer
  int i;
  for (i=1; i<6; i++)
  {
    push (lastPtrRef, i);
    lastPtrRef = &((*lastPtrRef)->next); // Advance to point to the new last pointer
  }
  return head;
}
    
void free_list (node_t** head)
// Version using a reference pointer to the head node
{
  while (*head != NULL)
  {
    node_t* oldPtr = *head;
    *head= (*head)->next;
    free (oldPtr);
    oldPtr = NULL; // setting an unused pointer to NULL (defensive style)
  }
  free (*head);
  *head = NULL;
}

void free_list2 (node_t* head)
// Version using a pointer to the head node
{
  while (head != NULL)
  {
    node_t* oldPtr = head;
    head = head->next;
    free (oldPtr);
    oldPtr = NULL;
  }
  free (head);
  head = NULL;
}


