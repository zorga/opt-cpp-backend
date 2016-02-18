#include <stdlib.h>

int main(int argc, char** argv)
{
  int* pTest = malloc(sizeof(int));
  *pTest = 4;
  //free(pTest);
  return 0;
}

