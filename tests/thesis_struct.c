#include <stdlib.h>

typedef struct student {
  char* firstname;
  char* lastname;
  int noma;
  float grade;
} student_t;

int main(int argc, char** argv)
{
  student_t john;
  john.firstname = "John";
  john.lastname = "Smith";
  john.noma = 16050900;
  john.grade = 12.0;

  return 0;
}

