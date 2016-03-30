#include <stdlib.h>

int main(int argc, char** argv)
{
  int* first = malloc(sizeof(int));
  int* second = malloc(sizeof(int));
  *first = 42;
  *second = 66;
  
  int** ptr = malloc(2*(sizeof(int*)));
  *ptr = first;
  *(ptr+1) = second;
  
  // free the allocated ressources
  free(first);
  free(second);
  free(ptr);

  return 0;
}

