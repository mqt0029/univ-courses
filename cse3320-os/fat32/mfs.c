#define _GNU_SOURCE

#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <signal.h>

#define delim " \t\n"

#define cmd_length 255        // The maximum command-line size
#define cmd_argc 5            // only supports five arguments
#define dir_entry_limit 16    // maximum number of file per directory

//enable boolean
typedef enum { false, true } bool;

//dummy-control variable
int i = 0;
bool exitflag = false;

/* ----------------------------------------------------------------------- */
/* FILE SYSTEM CONTAINERS */

//boot sector struct
typedef struct __attribute__((__packed__))
{
  uint8_t  BS_jmpBoot[ 3 ];     // 1 byte
  uint8_t  BS_OEMName[ 8 ];     // 1 byte
  uint16_t BPB_BytsPerSec;      // 2 bytes
  uint8_t  BPB_SecPerClus;      // 1 byte
  uint16_t BPB_RsvdSecCnt;      // 2 bytes
  uint8_t  BPB_NumFATs;         // 1 byte
  uint16_t BPB_RootEntCnt;      // 2 bytes
  uint16_t BPB_TotSec16;        // 2 bytes
  uint8_t  BPB_Media;           // 1 byte
  uint16_t BPB_FATSz16;         // 2 bytes
  uint16_t BPB_SecPerTrk;       // 2 bytes
  uint16_t BPB_NumHeads;        // 2 bytes
  uint32_t BPB_HiddSec;         // 4 bytes
  uint32_t BPB_TotSec32;        // 4 bytes
  uint32_t BPB_FATSz32;         // 4 bytes
  uint16_t BPB_ExtFlags;        // 2 bytes
  uint16_t BPB_FSVer;           // 2 bytes
  uint32_t BPB_RootClus;        // 4 bytes
  uint16_t BPB_FSInfo;          // 2 bytes
  uint16_t BPB_BkBootSec;       // 2 bytes
  uint8_t  BPB_Reserved[ 12 ];  //12 bytes
  uint8_t  BS_DrvNum;           // 1 byte
  uint8_t  BS_Reserved1;        // 1 byte
  uint8_t  BS_BootSig;          // 1 byte
  uint32_t BS_VolID;            // 4 bytes
  uint8_t  BS_VolLab[ 11 ];     //11 bytes
  uint8_t  BS_FilSysType[ 8 ];  // 8 bytes   
                                //90 bytes total  
} boot_sector;

//directory entry struct
typedef struct __attribute__((__packed__))
{
  uint8_t  DIR_Name[ 11 ];    //11 bytes
  uint8_t  DIR_Attr;          // 1 byte
  uint8_t  DIR_NTRes;         // 1 byte
  uint8_t  DIR_CrtTimeTenth;  // 1 byte
  uint16_t DIR_CrtTime;       // 2 bytes
  uint16_t DIR_CrtDate;       // 2 bytes
  uint16_t DIR_LstAccDate;    // 2 bytes
  uint16_t DIR_FstClusHI;     // 2 bytes
  uint16_t DIR_WrtTime;       // 2 bytes
  uint16_t DIR_WrtDate;       // 2 bytes
  uint16_t DIR_FstClusLO;     // 2 bytes
  uint32_t DIR_FileSize;      // 4 bytes
                              //32 bytes total
} dir_entry;

//file pointer to image
FILE *fs = NULL;

//boot sector and information
boot_sector bootsec;
uint16_t BPB_RsvdSecCnt;
uint16_t BPB_BytesPerSec;
uint8_t  BPB_SecPerClus;
uint32_t BPB_FATSz32;
uint8_t  BPB_NumFATs;

//directory container
dir_entry *directory;

//important addresses
uint32_t root_dir_address;
uint32_t working_dir;

/* ----------------------------------------------------------------------- */

int cluster_to_offset( uint32_t cluster )
{
  return ( ( cluster - 2 ) * BPB_BytesPerSec ) + root_dir_address;
}

void execute_command( char** command )
{
  char* function = command[ 0 ];
  
  if ( function == NULL )
  {
    // Empty input detected, do nothing.
  }
  else if ( !strcmp( function, "exit" ) )
  {
    exitflag = !exitflag;
  }
}

int main()
{
  char *command = (char*) malloc( cmd_length );
  directory = (dir_entry*)malloc(sizeof(dir_entry)*dir_entry_limit);

  while( !exitflag )
  {
    //clean up input and init
    memset(command,'\0',cmd_length);
    fflush(stdin);

    // Print out the mfs prompt
    printf ("mfs> ");

    // Read user input
    while( !fgets (command, cmd_length, stdin) );

    // String parsing variables
    char *token[cmd_argc];
    int   token_count = 0;                                 
                                                           
    // Pointer to point to the token parsed by strsep
    char *arg_ptr;                                         

    // Pointer to duplicated command for memory management                      
    char *working_str  = strndup( command, strlen( command ) );                

    // Tokenize the input stringswith whitespace used as the delimiter
    while ( ( ( arg_ptr = strsep( &working_str, delim ) ) != NULL) && ( token_count < cmd_argc ) )
    {
      token[ token_count ] = strndup( arg_ptr, cmd_length );
      if( strlen( token[ token_count ] ) == 0 )
      {
        token[ token_count ] = NULL;
      }
      token_count++;
    }
    
    // Free unnecessary vars
    free( working_str );

    // Execute command
    execute_command( token );
  }

  if ( fs != NULL )
  {
    fclose( fs );
  }
  free( command );
  free( directory );

  return 0;
}
