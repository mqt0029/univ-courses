// Tram, Minh
// mqt0029
// 1001540029
// 2019-05-13

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <errno.h>

#define line_length 255
#define param_count 5
#define delimiters " \t\n"
#define record_length 10

int append_history( char** target, char* toappend, int tracker )
{
  if ( tracker == (record_length - 1) )
  {
    free( target[0] );
    int rollup;
    for ( rollup = 0 ; rollup < record_length - 1 ; rollup++ )
    {
      target[rollup] = target[rollup + 1];
    }
    target[record_length - 1] = strndup( toappend, line_length );
  }
  else
  {
    target[tracker] = strndup( toappend, line_length );
    tracker++;
  }

  return tracker;
}

int append_pid( int* target, int pid, int tracker )
{
  if ( tracker == (record_length-1) )
  {
    int rollup;
    for ( rollup = 0 ; rollup < record_length - 1 ; rollup++ )
    {
      target[rollup] = target[rollup+1];
    }
    target[record_length - 1] = pid;
  }
  else
  {
    target[tracker] = pid;
    tracker++;
  }

  return tracker;
}

void listhistory(char** history)
{
  int list;
  for (list = 0; list < record_length; list++)
  {
    if (history[list] != NULL) printf("%d: %s", list, history[list]);
  }
}

void listpids(int* pids)
{
  int list;
  for (list = 0; list < record_length; list++)
  {
    if (pids[list] != -1) printf("%d: %d\n", list, pids[list]);
  }
}

int shell()
{
  int history_tracker = 0, pid_tracker = 0, i, selection;
  char *command = ( char* )malloc( line_length );
  char **cmd_history = ( char** )malloc( sizeof( char* ) * record_length );
  int *pid_history = ( int* )malloc( sizeof( int ) * record_length );

  for ( i = 0 ; i < record_length ; i++ ) 
  { 
    cmd_history[i] = NULL;
    pid_history[i] = -1; 
  }

  while ( 1 )
  {
    char** tokens = ( char** )malloc( sizeof( char* ) * ( param_count + 1 ) );
    char *token, *str, *marker;
    int token_count;

    token_count = 0;

    for ( i = 0 ; i < (param_count + 1) ; i++ ) 
    { 
      tokens[i] = NULL; 
    }

    //print shell prompt
    printf( "msh> " );

    //get all user input through stdin
    while ( !fgets( command, line_length, stdin ) );

    //separating string tokens
    marker = str = strdup( command );
    while ( ( token = strsep( &str, delimiters ) ) && ( token_count < param_count ) )
    {
      tokens[token_count] = strndup( token, line_length );
      if ( strlen( tokens[token_count] ) == 0 ) 
      { 
        free( tokens[token_count] );
        tokens[token_count] = NULL; 
      }
      token_count++;
    }

    //check exit
    if ( ( tokens[0] != NULL ) && ( !strcmp( tokens[0], "exit" ) || !strcmp( tokens[0], "quit" ) ) )
    {
      for ( i = 0 ; i < ( param_count + 1 ) ; i++ )
      {
        if ( tokens[i] != NULL )
        {
          free( tokens[i] );
          tokens[i] = NULL;
        } 
      }

      for ( i = 0 ; i < ( record_length ) ; i++ )
      {
        if ( cmd_history[i] != NULL) free( cmd_history[i] );
      }

      free( command );
      free( tokens );
      free( marker );
      free( cmd_history );
      free( pid_history );
      exit( EXIT_SUCCESS );
    }

    //command handler
    //ignoring empty commands
    pid_t curr_pid = fork();

    if ( curr_pid < 0 )
    {
      perror("fork failed");
    }
    else if ( !curr_pid )
    {
      if ( tokens[0] != NULL )
      {
        if ( !strcmp( tokens[0], "cd") )
        {
          exit( EXIT_SUCCESS );
        }
        else if ( !strcmp( tokens[0], "history" ) )
        {
          listhistory( cmd_history );
        }
        else if ( !strcmp( tokens[0], "listpids" ) )
        {
          listpids( pid_history );
        }
        else if ( tokens[0][0] == '!' )
        {
          int length = strlen( tokens[0] );
          char *number = &tokens[0][ length - ( length-1 ) ];

          selection = strtoul( number, NULL, 10 );

          if ( ( selection < record_length ) && ( cmd_history[selection] != NULL) )
          {

            char *submarker, *substr;
            submarker = substr = strdup( cmd_history[selection] );
            token_count = 0;

            memset( command, '\0', line_length );
            memcpy( command, cmd_history[selection], line_length );

            for ( i = 0 ; i < ( param_count + 1 ) ; i++ )
            {
              if ( tokens[i] != NULL )
              {
                free( tokens[i] );
                tokens[i] = NULL;
              } 
            }

            while ( ( token = strsep( &substr, delimiters ) ) && ( token_count < param_count ) )
            {
              tokens[token_count] = strndup( token, line_length );
              if ( strlen( tokens[token_count] ) == 0 ) 
              { 
                free( tokens[token_count] );
                tokens[token_count] = NULL; 
              }
              token_count++;
            }

            if ( tokens[0] != NULL )
            {
              if ( !strcmp( tokens[0], "cd") || tokens[0][0] == '!' )
              {
                exit( EXIT_SUCCESS );
              }
              else if ( !strcmp( tokens[0], "history" ) )
              {
                listhistory( cmd_history );
              }
              else if ( !strcmp( tokens[0], "listpids" ) )
              {
                listpids( pid_history );
              }
              else
              {
                execvp( tokens[0], tokens );
                perror( "msh" );
              }
            }

            free( submarker );            
          }
        }
        else
        {
          execvp( tokens[0], tokens );
          perror( "msh" );
        }

        exit( EXIT_SUCCESS );
      }
    }
    else
    {
      //append pid spawned
      pid_tracker = append_pid( pid_history, curr_pid, pid_tracker );
      
      int status;
      waitpid(curr_pid, &status, 0);
      if ( ( tokens[0] != NULL ) && ( !strcmp( tokens[0], "cd" ) ) )
      {
        chdir( tokens[1] );
      }
      fflush( NULL );
    }

    if ( strcmp( tokens[0], "history" ) != 0 && tokens[0][0] != '!' )
    {
      history_tracker = append_history( cmd_history, command, history_tracker );
    }

    //release malloc-ed chunks
    for ( i = 0 ; i < ( param_count + 1 ) ; i++ )
    {
      if ( tokens[i] != NULL )
      {
        free( tokens[i] );
        tokens[i] = NULL;
      } 
    }

    free( tokens );
    free( marker );
  }
  
  return 0;

}

int main( int argc, char const *argv[] )
{
  return shell();
}
