#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main()
{
    char * char_array[1024];

  int i = 0;

  for( i = 0; i < 1024; i++ )
  {
    char_array[i] = (char*)malloc( 1024 );
  }

  for( i = 1023; i >= 0; i-- )
  {
    free( char_array[i] );
  }

  for( i = 0; i < 1024; i++ )
  {
    char_array[i] = (char*)malloc( 10 );
  }

  for( i = 1023; i >= 0; i-- )
  {
    free( char_array[i] );
  }
  
  return 0;
}
