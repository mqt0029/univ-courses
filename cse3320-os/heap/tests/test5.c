#include <stdlib.h>
#include <stdio.h>

int main()
{
  printf("Running test 5 to test calloc() and realloc()\n");

  char * ptr1 = ( char * ) calloc(1, 2048 );

  free( ptr1 );

  char * ptr2 = ( char * ) calloc(1, 1024 );

  free( ptr2 );

  return 0;
}
