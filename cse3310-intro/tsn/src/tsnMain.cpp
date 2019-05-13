// Tram, Minh
// mqt0029
// 1001540029
// 2019-05-13

#include "tsnHeader.h"
#include "tsnCommunication.h"
#include "tsnGUI.h"

int main ( int argc, char* argv[] )
{
  init_system();

  thread backend_pub(background_publisher);
  thread responder(request_handler);
  thread ui_handler(primary_ui_handler);
  thread mailman(pull_mail);

  backend_pub.detach();
  responder.detach();
  mailman.detach();
  ui_handler.join();

  //Order of operation background > request > UI
  //means background will finish first before request finish before UI finish (if I'm right)
  return EXIT_SUCCESS;
}
