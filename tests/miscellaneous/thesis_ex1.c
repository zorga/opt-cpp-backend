#include <stdlib.h>

int main(int argc, char** argv)
{
  int* pTest = (int*) malloc(sizeof(int));
  *pTest = 4;
  free(pTest);
}

