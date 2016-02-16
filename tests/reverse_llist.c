#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void reverse(char* s) {
  char* end = s + (strlen(s) - 1);
  for(; end > s; --end, ++s) {
    (*s) ^= (*end);
    (*end) ^= (*s);
    (*s) ^= (*end);
  }
} 
  
int main() {
  char* x = malloc(20);
  strcpy(x, "Hello world!");
  reverse(x);
  return 0;
}

