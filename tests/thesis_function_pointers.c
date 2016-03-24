#include <stdlib.h>
#include <stdio.h>
/**
* A program to test the back-end with function pointers
* Written by Nicolas Ooghe
*/

// The funtion which the pointer will point to
void printName(const char* name)
{
  printf("Your name is %s\n", name);
}

int main(int argc, char** argv)
{
  //Declaring a function pointer and make it point to printName function
  void (*functionPointer)(const char*);
  functionPointer = &printName;
  printf("functionPointer points to : %p\n", functionPointer);
  //Calling the printName function using the function pointer
  (*functionPointer)("Nico"); 
}

