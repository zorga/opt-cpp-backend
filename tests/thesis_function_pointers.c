#include <stdlib.h>
#include <stdio.h>
/**
* A program to test the back-end with function pointers
* Written by Nicolas Ooghe
*/

void printName(const char* name)
{
  printf("Your name is %s\n", name);
}

int main(int argc, char** argv)
{
  //Declaring a function pointer and make it point to printName function
  void (*functionPointer)(const char*);
  functionPointer = &printName;
  //Calling the printName function using the function pointer
  (*functionPointer)("Nico"); 
}

