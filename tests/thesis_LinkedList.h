#ifndef _Thesis_LinkedList_H_
#define _Thesis_LinkedList_H_

typedef struct node node_t;

struct node {
  int data;
  node_t* next;
};

int InsertNth (node_t** head, int index, int data);

int GetNth (node_t* head, int i);

int pop (node_t** head);

void basicsCaller ();

void print_list_info (node_t* head);

int length (node_t* head);

int push (node_t** headRef, int newData);

node_t* buildOneTwoThree ();

void printList (node_t* head);

node_t* buildWithLocalRef ();

void free_list (node_t** head);

void free_list2 (node_t* head);

node_t* init (int initData);

#endif /* _Thesis_LinkedList_H_ */

