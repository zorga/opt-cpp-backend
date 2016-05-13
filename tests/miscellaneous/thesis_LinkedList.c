#include <stdio.h>
#include <stdlib.h>
#include "thesis_LinkedList.h" 

int main (int argc, char** argv)
{
  node_t* head = malloc (sizeof (node_t));
  head->data = 18;
  head->next = NULL;
  push (&head, 17);
  InsertSort(&head);
  free_list (&head);
  return 0;
}

void RemoveDuplicates (node_t* head)
/* the list pointed by 'head' is a list sorted in increasing order
   this function deletes the duplicate nodes from that list */
{
  node_t* current = head;
  if (!current)
  {
    fprintf (stderr, "RemoveDuplicates : uninitialized list\n");
    return;
  }

  while (current->next)
  {
    if (current->data == current->next->data)
    {
      node_t* nextNext = current->next->next;
      free (current->next);
      current->next = nextNext;
    }
    else
      current = current->next;
  }
}

void FrontBackSplit (node_t* source, node_t** frontRef, node_t** backRef)
/* Slip the list pointed by 'source' into two lists
   the first half of the list is pointed by *frontRef
   the second half of the lsit is pointed by *backRef */
{
  node_t* slowPtr;
  node_t* fastPtr;
  if (!source || !(source->next))
  {
    *frontRef = source;
    *backRef = NULL;
  }
  else
  {
    slowPtr = source;
    fastPtr = source->next;
    while (fastPtr)
    {
      fastPtr = fastPtr->next;
      if (fastPtr)
        slowPtr = slowPtr->next;
        fastPtr = fastPtr->next;
    }
    *frontRef = source;
    *backRef = slowPtr->next;
    slowPtr->next = NULL;
  }
}

void Append (node_t** aHead, node_t** bHead)
{
  if (!(*aHead))
    *aHead = *bHead;

  else
  {
    node_t* current = *aHead;

    while (current->next)
      current = current->next;

    current->next = *bHead;
    *bHead = NULL;
  }
}

int InsertSort (node_t** headRef)
  /* takes the list pointed by *headRef and sorts it in increasing order
     returns 0 if success, -1 otherwise */
{
  node_t* curr = *headRef;
  node_t* result = NULL; 
  node_t* next = NULL;

  if (!curr)
  {
    fprintf (stderr, "InsertSort : *headRef not initialized\n");
    return -1;
  }
  while (curr)
  {
    next = curr->next;
    SortedInsert (&result, curr);
    curr = next;
  }
  *headRef = result;

  return 0;
}

int SortedInsert (node_t** headRef, node_t* newNode)
  /* *headRef points to the head of a list sorted in increasing order.
     inserts newNode into the correct position in the list (in a way that keep
     the ordering of the list)
     if *headRef is NULL, makes newNode point to it and makes *headRef points to
     newNode so the result is a list containing only newNode */
{
  node_t dummy;
  node_t* curr = &dummy;
  dummy.next = *headRef;

  while (curr->next && curr->next->data < newNode->data)
    curr = curr->next;

  newNode->next = curr->next;
  curr->next = newNode;
  *headRef = dummy.next;

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
  node_t* head = init (97777778);
  push(&head, 777777);
  push(&head, 83293);
  push(&head, 8989);
  push(&head, 43);
  push(&head, 3);
  return head;
}

int printList (node_t* head)
  /* prints the informations of the list whose head node is pointed by head
     it prints the address of the nodes along with their data
     returns 0 if success, -1 otherwise; */
{
  if (!head)
  {
    fprintf (stderr, "printList : NULL pointer error\n");
    return -1;
  }

  int count = 0;
  node_t* current = head;
  printf ("List info : \n");
  for (current = head; current != NULL; current = current->next)
  {
    printf ("Node %d : %p, Data : %d\n", count, current, current->data);
    count++;
  }
  printf ("Length of the list : %d\n", count);
  return 0;
}

node_t* buildWithLocalRef (int a)
{
  /* head pointer set to NULL because it will be the last node at the end
     of the function call */
  node_t* head = NULL;
  node_t** lastPtrRef = &head; // Start out pointing to the head pointer

  for (int i=0; i<5; i++)
  {
    srand (a*i*4);
    push (lastPtrRef, (rand() % 1000));
    //push (lastPtrRef, i);
    lastPtrRef = &((*lastPtrRef)->next); // Advance to point to the new last pointer
  }
  return head;
}

int free_list (node_t** headRef)
  /* delete and free all the memory used by the list
     using a reference pointer to the head of the list
     returns 0 if success, -1 otherwise */
{
  if (!(*headRef))
  {
    fprintf(stderr, "free_list : NULL pointer error\n");
    return -1;
  }

  while (*headRef != NULL)
  {
    node_t* oldPtr = *headRef;
    *headRef = (*headRef)->next;
    free (oldPtr);
    oldPtr = NULL; // setting an unused pointer to NULL (defensive style)
  }
  free (*headRef);
  *headRef = NULL;
  return 0;
}

int free_list2 (node_t* head)
  /* delete and free all the memory used by the list
     using a pointer to the head of the list
     returns 0 if success, -1 otherwise */
{
  if (!head)
  {
    fprintf (stderr, "free_list : NULL pointer error\n");
    return -1;
  }

  while (head != NULL)
  {
    node_t* oldPtr = head;
    head = head->next;
    free (oldPtr);
    oldPtr = NULL;
  }
  free (head);
  head = NULL;
  return 0;
}


