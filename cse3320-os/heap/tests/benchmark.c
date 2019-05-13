#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
  time_t start, end;
  double difference;
  start = time(NULL);
  
  /*things I need to time*/
  char * char_array[1024];

  int i = 0;

  srand( time( 0 ) );

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
    char_array[i] = (char*)malloc( 1024 );
  }

  for( i = 1023; i >= 0; i-- )
  {
    free( char_array[i] );
  }

  char * heap = (char*)malloc( 1024*1024 );
  free( heap );

  for( i = 0; i < 1024; i++ )
  {
    if( i % 2 == 0 )
      char_array[i] = (char*)malloc( 512 );
    else
      char_array[i] = NULL;
  }

  for( i = 0; i < 1024; i++ )
  {
    if( char_array[i] )
      free( char_array[i] );
  }

  for( i = 0; i < 1024; i++ )
  {
      char_array[i] = (char*)malloc( 4096 );
  }

  for( i = 0; i < 1024; i++ )
  {
      free( char_array[i] );
  }

  for( i = 0; i < 1024; i++ )
  {
      char_array[i] = (char*)malloc( 8192 );
  }

  for( i = 512; i >= 0; i-- )
  {
    free( char_array[i] );
  }

  for( i = 513; i < 1024; i++ )
  {
    free( char_array[i] );
  }
  
  /* timing ends */
  end = time(NULL);
  if (end != start)
  { 
    difference = difftime(end, start);
  }
  printf("%d seconds\n", (int)difference);
  return 0;
}
