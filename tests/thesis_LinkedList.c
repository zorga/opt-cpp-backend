#include <stdio.h>
#include <stdlib.h>
#include "thesis_LinkedList.h" 

#define PRINT_PTR (1)

int main (int argc, char** argv)
/* Put tests on list here */
{
  node_t* head = buildWithLocalRef ();
  // LIST BEFORE TESTS :
  if (PRINT_PTR)
  {
    printList (head);
  }
  //TESTS :
  int i = 0;
  int j = 9;
  printf ("Data of the %dth node of the list : %d\n", i, GetNth(head, i));
  printf ("Data of the %dth node of the list : %d\n", j, GetNth(head, j));
  InsertNth (&head, 9, 42);
  InsertNth (&head, 10, 43);
  InsertNth(&head, 43, 98);
  InsertNth(&head, 12, 666666666);
  //PRINT LIST :
  if (PRINT_PTR)
  {
    printList (head);
  }

  free_list (&head);
  return 0;
}

int InsertNth(node_t** head, int index, int data)
/* insert a new node in the list whose head is pointed by *head at index 
   and with 'data' as data field
   returns 0 if succees
   returns -1 in case of failure
*/
{
  node_t* curr = *head;

  if (index > length (curr))
  {
    fprintf (stderr, "InsertNth : index out of range !\n");
    return -1;
  }

  if (!curr)
    return -1;

  for (int i = 0; i < index-1; i++)
    curr = curr->next; 

  node_t* newNode = (node_t*) malloc (sizeof (node_t));
  if (!newNode)
    return -1;

  newNode->data = data;
  newNode->next = curr->next;
  curr->next = newNode;

  return 0;
}

int GetNth (node_t* head, int i)
/* returns the data contained in the ith node of the list whose head is pointed
   by the head pointer.
   the nodes are in the range [0..length (head) -1]
   returns -1 in case of error */
{
  if (!head)
    return -1;

  else if (i >= length (head))
    return -1;

  node_t* curr = head;
  for (int j = 0; j < i; j++)
    curr = curr -> next;
  
  return (curr->data);
}

int pop (node_t** headRef)
/* deletes the head node of the list and returns its data
   returns -1 in case of error */
{
  node_t* head = *headRef;
  if (!head)
    return -1;

  int ret = head->data;
  *headRef = head->next;
  free (head);
    head = NULL;

  return ret;
}
  
int length (node_t* head)
/* returns the length of the list whose head node is pointed by 'head'
   returns -1 in case of error */
{
  if (!head)
    return -1;

  int len = 1;
  node_t* curr = head;
  while (curr->next)
  {
    len++;
    curr = curr->next;
  }
  return len;
}

int push (node_t** headRef, int newData)
/* insert a new node at the beginning of the list with 'newData' as data 
   returns 0 if the function succeeds 
   returns -1 on failure */
{
  node_t* newHead = (node_t*) malloc (sizeof (node_t)); 
  if (!newHead)
    return -1;

  newHead->data = newData;
  newHead->next = *headRef;
  // changing a Pointer using a Reference Pointer (Pointer to Pointer)
  *headRef = newHead;
  return 0;
}

node_t* init (int initData)
/* Initialize a new list with 'initData' as the first node dada */
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
/* prints the informations of the list whose head node is pointed by head
   it prints the address of the nodes along with their data */
{
  if (!head)
    perror("unitialized list");

  int count = 0;
  node_t* current = head;
  printf ("List info : \n");
  for (current = head; current != NULL; current = current->next)
  {
    printf ("Node %d : %p, Data : %d\n", count, current, current->data);
    count++;
  }
  printf ("Length of the list : %d\n", count);
}

node_t* buildWithLocalRef ()
{
  /* head pointer set to NULL because it will be the last node at the end
  of the function call */
  node_t* head = NULL;
  node_t** lastPtrRef = &head; // Start out pointing to the head pointer

  for (int i=0; i<10; i++)
  {
    srand (i*4);
    push (lastPtrRef, rand());
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


