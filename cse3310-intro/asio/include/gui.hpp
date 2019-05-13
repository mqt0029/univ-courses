#ifndef NCURSES_GUI_HPP
#define NCURSES_GUI_HPP

#define RECOMMENDED_WIDTH   80
#define RECOMMENDED_HEIGHT  40

#include <ncurses.h>
#include <iostream>
#include <cassert>
#include <thread>
#include <mutex>

//----------------------------------------------------------------------
// Convenience variables

WINDOW *primary_screen; //pointer to terminal
WINDOW *message_box;    //pointer to input box
WINDOW *display_box;    //pointer to incoming message box

// dimension controlling variables
int maxx, maxy, newmaxx, newmaxy;
int current_line = 1;

bool exitflag = false;
bool freeze   = false;

std::mutex safety_lock;

//----------------------------------------------------------------------
// Function Definition

std::string get_string_from_window(WINDOW *target, int column_limit)
{
  std::string input;
  input.clear();

  nocbreak();
  echo();

  int ch = wgetch(target);
  while ( ch != '\n' )
  {
    if ( ch >= 32 && ch <= 126 )
      input.push_back( ch );

    ch = wgetch(target);
  }

  input.push_back( '\0' );

  cbreak();
  noecho();

  return input;
}

void make_message_box()
{
  wclear( message_box );
  box( message_box, 0, 0 );
  wattron( message_box, A_REVERSE );
  mvwprintw( message_box, 0, 0, "MESSAGE" );
  wattroff( message_box, A_REVERSE );
  wrefresh( message_box );
  curs_set( 1 );
  wmove( message_box, 1, 1 );
}

void make_display_box()
{
  box( display_box, 0, 0 );
  wattron( display_box, A_REVERSE );
  mvwprintw( display_box, 0, 0, "CHAT ROOM" );
  wattroff( display_box, A_REVERSE );
  wrefresh( display_box );
  curs_set( 0 );
}

void gui_init()
{
  primary_screen = initscr();
  
  //empty screen and remove cursor
  clear();
  noecho();
  cbreak();
  curs_set(0);
  //scrollok( display_box, TRUE );

  //check terminal dimension
  getmaxyx( primary_screen, maxy, maxx );
  assert( maxx >= RECOMMENDED_WIDTH );
  assert( maxy >= RECOMMENDED_HEIGHT );

  //display main GUI
  //display input box
  message_box = subwin( primary_screen, 4, maxx, maxy - 4, 0 );
  make_message_box();

  //display incoming messages box
  display_box = subwin( primary_screen, maxy - 4, maxx, 0, 0 );
  make_display_box();
}

//----------------------------------------------------------------------

#endif