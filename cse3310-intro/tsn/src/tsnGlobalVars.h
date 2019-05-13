#ifndef TSNGLOBALVARS_H
#define TSNGLOBALVARS_H

#include "tsnHeader.h"

//default file names for local data storage
char local_user_data[] = ".tsn";                    //default user info file
char local_content_data[] = ".localcontent";        //default local content file

//controlling variables, marked volatile for accuracy
volatile bool request_available = true;               //changed to false for 1 min after a request is made
volatile int timelapse_counter = 0;                   //clock checking, ++ every 30 sec
volatile serial_number local_serial_number = 1;       //(flagged volatile), serial number counter for local posts
struct timespec universe_clock;                       //time since epoch watchdog

//local content
user_information local_user;
vector <response> local_content;

//gui variables
const int choice_limit = 9;
array<string, choice_limit> choices = {"1. List users", "2. User information", "3. Post", "4. Request", "5. Refresh", "6. Send Message", "7. Exit", "--- Local User", "--- Edit Local User"};
WINDOW* screen;
WINDOW* menubox;
WINDOW* statusbox;
WINDOW* chatbox;
int maxy, maxx, newmaxy, newmaxx;
unsigned int menu_selection = 0, status_selection = 0;
bool exited = false, freezemenu = false;

//information storage vectors
//dump vectors will collect all available, including duplicates, and filtered will remove excess contents
vector <user_information> userinfo_dump;
vector <response> response_dump;
vector <response> floating_dump;
vector <request> request_dump;
vector <private_message> message_dump;

vector <user_information> filtered_user;
vector <response> filtered_response;
vector <response> filtered_floating;
vector <request> filtered_request;
vector <private_message> filtered_message;

//ugly chunks that handles comms between nodes _______Sub are subscribers and __________Pub are publishers
dds_io<user_information,
      user_informationSeq,
      user_informationTypeSupport_var,
      user_informationTypeSupport,
      user_informationDataWriter_var,
      user_informationDataWriter,
      user_informationDataReader_var,
      user_informationDataReader> userinf_sub =
dds_io<user_information,
      user_informationSeq,
      user_informationTypeSupport_var,
      user_informationTypeSupport,
      user_informationDataWriter_var,
      user_informationDataWriter,
      user_informationDataReader_var,
      user_informationDataReader> ((char*)"user_information",false,true);

dds_io<response,
      responseSeq,
      responseTypeSupport_var,
      responseTypeSupport,
      responseDataWriter_var,
      responseDataWriter,
      responseDataReader_var,
      responseDataReader> response_sub =
dds_io<response,
      responseSeq,
      responseTypeSupport_var,
      responseTypeSupport,
      responseDataWriter_var,
      responseDataWriter,
      responseDataReader_var,
      responseDataReader> ((char*)"response",false,true);

dds_io<request,
       requestSeq,
       requestTypeSupport_var,
       requestTypeSupport,
       requestDataWriter_var,
       requestDataWriter,
       requestDataReader_var,
       requestDataReader> request_sub =
dds_io<request,
       requestSeq,
       requestTypeSupport_var,
       requestTypeSupport,
       requestDataWriter_var,
       requestDataWriter,
       requestDataReader_var,
       requestDataReader> ((char*)"request",false,true);

dds_io<private_message,
      private_messageSeq,
      private_messageTypeSupport_var,
      private_messageTypeSupport,
      private_messageDataWriter_var,
      private_messageDataWriter,
      private_messageDataReader_var,
      private_messageDataReader> private_message_sub =
dds_io<private_message,
      private_messageSeq,
      private_messageTypeSupport_var,
      private_messageTypeSupport,
      private_messageDataWriter_var,
      private_messageDataWriter,
      private_messageDataReader_var,
      private_messageDataReader> ((char*)"private_message",false,true);

dds_io<user_information,
     user_informationSeq,
     user_informationTypeSupport_var,
     user_informationTypeSupport,
     user_informationDataWriter_var,
     user_informationDataWriter,
     user_informationDataReader_var,
     user_informationDataReader> userinf_pub =
dds_io<user_information,
     user_informationSeq,
     user_informationTypeSupport_var,
     user_informationTypeSupport,
     user_informationDataWriter_var,
     user_informationDataWriter,
     user_informationDataReader_var,
     user_informationDataReader> ((char*)"user_information",true,false);

dds_io<request,
      requestSeq,
      requestTypeSupport_var,
      requestTypeSupport,
      requestDataWriter_var,
      requestDataWriter,
      requestDataReader_var,
      requestDataReader> request_pub =
dds_io<request,
      requestSeq,
      requestTypeSupport_var,
      requestTypeSupport,
      requestDataWriter_var,
      requestDataWriter,
      requestDataReader_var,
      requestDataReader> ((char*)"request",true,false);

dds_io<response,
      responseSeq,
      responseTypeSupport_var,
      responseTypeSupport,
      responseDataWriter_var,
      responseDataWriter,
      responseDataReader_var,
      responseDataReader> response_pub =
dds_io<response,
      responseSeq,
      responseTypeSupport_var,
      responseTypeSupport,
      responseDataWriter_var,
      responseDataWriter,
      responseDataReader_var,
      responseDataReader> ((char*)"response",true,false);

dds_io<private_message,
      private_messageSeq,
      private_messageTypeSupport_var,
      private_messageTypeSupport,
      private_messageDataWriter_var,
      private_messageDataWriter,
      private_messageDataReader_var,
      private_messageDataReader> private_message_pub =
dds_io<private_message,
      private_messageSeq,
      private_messageTypeSupport_var,
      private_messageTypeSupport,
      private_messageDataWriter_var,
      private_messageDataWriter,
      private_messageDataReader_var,
      private_messageDataReader> ((char*)"private_message",true,false);

#endif
