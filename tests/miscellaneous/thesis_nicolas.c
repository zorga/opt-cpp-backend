#include <stdlib.h>
#include <stdio.h>

int main(int argc, char** argv)
{
  char* cName = (char*) malloc(8*sizeof(char));
  *cName = 'N';
  *(cName+1) = 'i';
  *(cName+2) = 'c';
  *(cName+3) = 'o';
  *(cName+4) = 'l';
  *(cName+5) = 'a';
  *(cName+6) = 's';
  *(cName+7) = '\0';
  printf("My name is : %s\n", cName);
  free(cName);

  return 0;
}

