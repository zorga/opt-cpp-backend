#ifndef _Thesis_LinkedList_H_
#define _Thesis_LinkedList_H_

typedef struct node node_t;

struct node {
  int data;
  node_t* next;
};

int addTail (node_t* head, int newData);

void RemoveDuplicates (node_t* head);

void FrontBackSplit (node_t* source, node_t** frontRef, node_t** backRef);

int InsertSort (node_t** headRef);

int SortedInsert (node_t** headRef, node_t* newNode);

int InsertNth (node_t** head, int index, int data);

int GetNth (node_t* head, int i);

int pop (node_t** head);

void basicsCaller ();

int length (node_t* head);

int push (node_t** headRef, int newData);

node_t* buildOneTwoThree ();

int printList (node_t* head);

node_t* buildWithLocalRef (int a);

void Append (node_t** aHead, node_t** bHead);

int free_list (node_t** head);

int free_list2 (node_t* head);

node_t* init (int initData);

#endif /* _Thesis_LinkedList_H_ */

