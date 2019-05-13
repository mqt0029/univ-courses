// Tram, Minh
// mqt0029
// 1001540029
// 2019-05-13

#ifndef TSNGUI_H
#define TSNGUI_H

#include "tsnHeader.h"
#include "tsnGlobalVars.h"
#include "tsnCommunication.h"

#define RECOMMENDED_WIDTH 43
#define RECOMMENDED_HEIGHT 80

//get user input string from window, currently not handling errors
std::string getstringw(WINDOW *statusbox)
{
    std::string input;
    int thisy, thisx;
    // let the terminal do the line editing
    nocbreak();
    echo();
    // this reads from buffer after <ENTER>, not "raw"
    // so any backspacing etc. has already been taken care of
    int ch = wgetch(statusbox);
    while ( ch != '\n' )
    {
        input.push_back( ch );
        ch = wgetch(statusbox);
        getyx(statusbox, thisy, thisx);
        if (thisx >= maxx-2)
        {
          thisx = 1;
          thisy+= 1;
          wmove(statusbox, thisy, thisx);
        }
    }
    // restore your cbreak / echo settings here
    cbreak();	/* Line buffering disabled. pass on everything */
    noecho();
    return input;
}

unsigned int getintunsignedw(WINDOW *menu_win)
{
    string input;
    input.clear();
    // let the terminal do the line editing
    nocbreak();
    echo();
    // this reads from buffer after <ENTER>, not "raw"
    // so any backspacing etc. has already been taken care of
    int ch = wgetch(menu_win);
    while ( ch != '\n' )
    {
        input.push_back(ch);
        ch = wgetch(menu_win);
    }
    // restore your cbreak / echo settings here
    cbreak();	/* Line buffering disabled. pass on everything */
    noecho();
    return stoi(input, nullptr, 10);
}

//find correct width for original box
int longest(const array<string, choice_limit> &target)
{
  unsigned int width = 0;
  for (string s : target)
  {
    if (s.length() > width)
    {
      width = s.length();
    }
  }
  return width + 2;
}

//ncurses box redraws for respective boxes
void makeboxstatus()
{
  box(statusbox, 0, 0);
  wattron(statusbox, A_REVERSE);
  mvwprintw(statusbox, 0, 0, "CURRENT OPERATION");
  wattroff(statusbox, A_REVERSE);
  wrefresh(statusbox);
}

void makeboxmessage()
{
  box(chatbox, 0, 0);
  wattron(chatbox, A_REVERSE);
  mvwprintw(chatbox, 0, 0, "MESSAGE");
  wattroff(chatbox, A_REVERSE);
  wrefresh(chatbox);
}

//startup original GUI
void initmenu()
{
  int menuwidth = longest(choices), menuheight = choice_limit + 2;

  menubox = subwin(screen, menuheight, menuwidth, 0, 0);
  box(menubox, 0, 0);

  wattron(menubox, A_REVERSE);
  mvwprintw(menubox, 0, 0, "MENU");
  wattroff(menubox, A_REVERSE);

  for (int i = 1; i < choice_limit+1; i++)
  {
    mvwprintw(menubox, i, 1, choices[i-1].c_str());
  }
  wrefresh(menubox);
}

void initchatbox()
{
  int chatbox_w = maxx-longest(choices)-1, chatbox_h = choice_limit + 2;
  chatbox = subwin(screen, chatbox_h, chatbox_w, 0, longest(choices) + 1);
  makeboxmessage();
}

void initstatusbox()
{
  int status_w = maxx, status_h = maxy - (choice_limit + 3);
  statusbox = subwin(screen, status_h, status_w, choice_limit + 2, 0);
  makeboxstatus();
}

//function to update menu as part of the "aninamtion"
void update_menu(int selection)
{
  for (int i = 0; i < choice_limit; i++)
  {
    if (i == selection)
    {
      wattron(menubox, A_REVERSE);
      mvwprintw(menubox, i+1, 1, choices[i].c_str());
      wattroff(menubox, A_REVERSE);
    }
    else
    {
      mvwprintw(menubox, i+1, 1, choices[i].c_str());
    }
  }
  wrefresh(menubox);
}

//handle saving local user and content to file when exit the program
void exit_procedure()
{
  ofstream local(local_content_data, ofstream::trunc);
  local << local_content.size() << endl;
  for (unsigned int i = 0; i < local_content.size(); i++)
  {
    local << local_content[i].uuid << endl;
    local << local_content[i].post_id << endl;
    local << local_content[i].post_body << endl;
    local << local_content[i].date_of_creation << endl;
    local << "0" << endl;
    local << "0" << endl;
  }
  local.close();

  ofstream destination(local_user_data, ofstream::trunc);
  destination.seekp(ios_base::beg);
  destination << local_user.uuid << endl;
  destination << local_user.date_of_birth << endl;
  destination << local_user.first_name << endl;
  destination << local_user.last_name << endl;
  destination << local_user.number_of_highest_post << endl;
  destination << local_user.interests.length() << endl;
  for (unsigned int i = 0; i < local_user.interests.length(); i++)
  {
    destination << local_user.interests[i] << endl;
  }
  destination.close();
}

//show available user via their uuid
void list_users()
{
  int line = 1;

  if (filtered_user.size() == 0) return;
  else
    for (struct user_information u : filtered_user)
    {
      if (line == 1) mvwprintw(statusbox, line, 1, "---(local)%d. %s\n", line, u.uuid);
      else mvwprintw(statusbox, line, 1, "%d. %s\n", line, u.uuid);
      line++;
    }

  mvwprintw(statusbox, line, 1, "Operation completed.");
}

//update submenu as program navigates through options
void update_submenu_sui() //sui = show_user_info()
{
  werase(statusbox);
  mvwprintw(statusbox, 1, 1, "Select a user");
  for (unsigned int i = 1; i < filtered_user.size(); i++)
  {
    if (i == status_selection)
    {
      wattron(statusbox, A_REVERSE);
      mvwprintw(statusbox, i+1, 1, filtered_user.at(i).uuid);
      wattroff(statusbox, A_REVERSE);
    }
    else
    {
      mvwprintw(statusbox, i+1, 1, filtered_user.at(i).uuid);
    }
  }
  makeboxstatus();
}

//show details of selected user
void list_details(struct user_information target)
{
  time_t temp = target.date_of_birth;
  werase(statusbox);     //clear the window
  mvwprintw(statusbox, 1, 1, "-----USER INFO BEGIN-----\n");
  wprintw(statusbox, "  UUID: %s\n",target.uuid);
  wprintw(statusbox, "  Name: %s %s\n", DDS::string_dup(target.first_name), DDS::string_dup(target.last_name));//i dont know why string_dup makes it work but it does
  wprintw(statusbox, "  Date of Birth: %s\n", ctime(&temp));
  wprintw(statusbox, "  Highest post count: %i\n", target.number_of_highest_post);
  wprintw(statusbox, "  Interest(s): \n");
  for (unsigned int i = 0; i < target.interests.length(); i++)
  {
    wprintw(statusbox, "     %i. %s\n",i+1, DDS::string_dup(target.interests[i]));
  }
  wprintw(statusbox, "  -----USER INFO END-----\n");
  makeboxstatus();
}

//gui controlled for showing user information
void show_user_info()
{
  bool quit_info = false;

  if (filtered_user.size() <= 1)
  {
    werase(statusbox);
    mvwprintw(statusbox, 1, 1, "There is no user to show. Try refresh?");
    makeboxstatus();
    return;
  }

  status_selection = 1;
  update_submenu_sui();

  keypad(statusbox, TRUE);

  while (!quit_info)
  {
    int c_status = wgetch(statusbox);
    switch(c_status)
    {
      case KEY_UP:
        if (status_selection == 1) status_selection = filtered_user.size()-1;
        else status_selection--;
        update_submenu_sui();
        break;

      case KEY_DOWN:
        if (status_selection == filtered_user.size() - 1) status_selection = 1;
        else status_selection++;
        update_submenu_sui();
        break;

      case 10:
      {
        struct user_information output = filtered_user.at(status_selection);
        list_details(output);
        quit_info = !quit_info;
        break;
      }

      case 27:
        quit_info = !quit_info;
        break;
    }
  }
  status_selection = 0;
}

//funtion to make new post
void post()
{
  struct response newpost;
  strncpy(newpost.uuid, local_user.uuid, sizeof(newpost.uuid));
  newpost.uuid[sizeof(newpost.uuid) - 1] = '\0';
  newpost.post_id = local_serial_number;
  local_serial_number++;

  string body;
  werase(statusbox);

  if (local_content.size() >= 1)
  {
    makeboxstatus();
    mvwprintw(statusbox, 1, 1, "Does this post have a parent? (Y/y or N/n)");
    char answer = wgetch(statusbox);
    if (answer == 'y' || answer == 'Y')
    {
      makeboxstatus();
      mvwprintw(statusbox, 2, 1, "Enter post_id of the parent post (may not exists): ");
      unsigned int target_id = getintunsignedw(statusbox);
      for (struct response r : local_content)
      {
        if (r.post_id == target_id)
        {
          strncpy(newpost.parent_post.owner_uuid, r.uuid, sizeof(newpost.parent_post.owner_uuid));
          newpost.parent_post.owner_uuid[sizeof(newpost.parent_post.owner_uuid)-1] = '\0';
          newpost.parent_post.post_id = r.post_id;
          r.child_posts.length(r.child_posts.length()+1);
          strncpy(r.child_posts[r.child_posts.length() - 1].owner_uuid, newpost.uuid, sizeof(r.child_posts[r.child_posts.length() - 1].owner_uuid));
          r.child_posts[r.child_posts.length() - 1].owner_uuid[sizeof(r.child_posts[r.child_posts.length() - 1].owner_uuid)-1] = '\0';
          r.child_posts[r.child_posts.length() - 1].post_id = newpost.post_id;
        }
      }
    }
    else if (answer == 'n' || answer == 'N')
    {
      //do nothing
    }
  }
  makeboxstatus();
  mvwprintw(statusbox, 3, 1, "What is the post content? ");
  curs_set(1);

  body = getstringw(statusbox);
  newpost.post_body = DDS::string_dup(body.c_str());
  clock_gettime(CLOCK_REALTIME,&universe_clock);
  newpost.date_of_creation = (long)universe_clock.tv_sec;

  if (body.length() == 0)
  {
    makeboxstatus();
    mvwprintw(statusbox, 20, 1, "Empty input, post is ignored.");
    local_serial_number--;
  }
  else
  {
    makeboxstatus();
    local_content.push_back(newpost);
    mvwprintw(statusbox, 20, 1, "Operation completed successfully.");
    curs_set(0);
  }
}

//function to send request. Verified by stalker program
void send_request(WINDOW *menu_win)
{
  int tries = 0;
  werase(menu_win);                                                       //show requestable targets
  request_available = false;                                              //limit to 1 per min
  request package;                                                        //struct to process request and init requester info
  strncpy(package.uuid, local_user.uuid, sizeof(package.uuid));           //attach requester uuid
  package.uuid[sizeof(package.uuid)-1] = '\0';                            //null terminate uuid
  int temp;
  unsigned int num_target;                                                //number of node targeted
  for (unsigned int c = 1; c < filtered_user.size(); c++)
  {
    mvwprintw(menu_win, 1+c, 1, "%d. %s", c, filtered_user.at(c).uuid);
    temp = c+2;
  }
  makeboxstatus();
  mvwprintw(menu_win, 1, 1, "Requesting from how many nodes? ");
  wrefresh(statusbox);
  num_target = getintunsignedw(menu_win);
  package.user_requests.length(num_target);                               //set length for node_request
  wmove(statusbox, temp, 1);
  tries += num_target;
  for (unsigned int i = 0; i < num_target; i++)                           //loop for each UUID x number of serial requested
  {                                                                       //skips cin wait for >1 target, need resolve
    unsigned int target_uuid;                                             //init fulfiller uuid as an index
    int target_count;                                                     //init fulfiller possible node_request
    wprintw(menu_win, "  Target %i UUID: ", i+1);
    target_uuid = getintunsignedw(menu_win);
    strncpy(package.user_requests[i].fulfiller_uuid, filtered_user[target_uuid].uuid, sizeof(package.user_requests[i].fulfiller_uuid));  //grab fulfiller uuid from vector
    package.user_requests[i].fulfiller_uuid[sizeof(package.user_requests[i].fulfiller_uuid) - 1] = '\0';                                 //null terminated uuid
    temp++;
    makeboxstatus();
    wmove(statusbox, temp, 1);

    wprintw(menu_win, "    Number of post requested: ");
    target_count = getintunsignedw(menu_win);
    tries *= target_count;
    package.user_requests[i].requested_posts.length(target_count);        //set length for fulfiller number of requested posts
    temp++;
    makeboxstatus();
    wmove(statusbox, temp, 1);
    for (int j = 0; j < target_count; j++)
    {
      int serial;
      wprintw(menu_win, "       Serial of request #%i: ", j+1);
      serial = getintunsignedw(menu_win);
      package.user_requests[i].requested_posts[j] = serial;
      temp++;
      makeboxstatus();
      wmove(statusbox, temp, 1);
    }
  }

  //Request publisher, confirmed working by stalker program

  request_pub.publish(package);
  werase(menu_win);
  mvwprintw(menu_win, 1, 1, "Request made successfully. Grabbing responses...");
  mvwprintw(menu_win, 2, 1, "=========RESPONSE BEGIN==========\n");
  vector<response> from_request = response_sub.recv();
  for (unsigned int i = 0; i < from_request.size(); i++)
  {
    wprintw(menu_win, "  Response: \n", i+1);
    wprintw(menu_win, "     From: %s: \n", from_request[i].uuid);
    wprintw(menu_win, "     Serial Number: %i: \n", from_request[i].post_id);
    wprintw(menu_win, "     Content: %s: \n", from_request[i].post_body);
    wprintw(menu_win, "     Time: %i: \n\n", from_request[i].date_of_creation );
  }
  wprintw(menu_win, "==========RESPONSE END==========\n" );
  makeboxstatus();
}

//GUI helper to call on the actual requesting function
void make_request()
{
  if (!request_available)
  {
    mvwprintw(statusbox, 1, 1, "Requests are currently unavailable. Try again after %d seconds.", 30);
    makeboxstatus();
    return;
  }
  else if (filtered_user.size() <= 1)
  {
    mvwprintw(statusbox, 1, 1, "No user found on the network. Try refresh?");
    makeboxstatus();
    return;
  }
  else
  {
    send_request(statusbox);
  }
}

//function to update GUI to input outgoing message
void compose_message(struct user_information r, struct user_information s)
{
  curs_set(1);
  struct private_message mail;
  strncpy(mail.receiver_uuid, r.uuid, sizeof(mail.receiver_uuid));
  mail.receiver_uuid[sizeof(mail.receiver_uuid)-1] = '\0';
  strncpy(mail.sender_uuid, s.uuid, sizeof(mail.sender_uuid));
  mail.sender_uuid[sizeof(mail.sender_uuid)-1] = '\0';
  werase(statusbox);
  makeboxstatus();
  mvwprintw(statusbox, 1, 1, "Message: ");
  string body = getstringw(statusbox);
  mail.message_body = DDS::string_dup(body.c_str());
  clock_gettime(CLOCK_REALTIME,&universe_clock);
  mail.date_of_creation = (long)universe_clock.tv_sec;

  if (body.length() == 0)
  {
    makeboxstatus();
    mvwprintw(statusbox, 20, 1, "Empty input, message is not posted.");
  }
  else
  {
    makeboxstatus();
    private_message_pub.publish(mail);
    mvwprintw(statusbox, 20, 1, "Operation completed successfully.");
    curs_set(0);
  }
}

//helper to call on the function above
void messenger()
{
  bool quit_info = false;

  if (filtered_user.size() <= 1)
  {
    werase(statusbox);
    makeboxstatus();
    mvwprintw(statusbox, 1, 1, "There is no user to send message to. Try refresh?");
    return;
  }

  status_selection = 1;
  update_submenu_sui();

  keypad(statusbox, TRUE);

  while (!quit_info)
  {
    int c_status = wgetch(statusbox);
    switch(c_status)
    {
      case KEY_UP:
        if (status_selection == 1) status_selection = filtered_user.size()-1;
        else status_selection--;
        update_submenu_sui();
        break;

      case KEY_DOWN:
        if (status_selection == filtered_user.size() - 1) status_selection = 1;
        else status_selection++;
        update_submenu_sui();
        break;

      case 10:
      {
        struct user_information receiver = filtered_user.at(status_selection);
        struct user_information sender = local_user;
        compose_message(receiver, sender);
        quit_info = !quit_info;
        break;
      }

      case 27:
        quit_info = !quit_info;
        break;
    }
  }
  status_selection = 0;
}

//display local user information
void local_information()
{
  werase(statusbox);
  std::time_t temp = local_user.date_of_birth;
  mvwprintw(statusbox, 1, 1, "-----LOCAL USER INFO-----\n");
  wprintw(statusbox, "  UUID: %s\n",local_user.uuid);
  wprintw(statusbox, "  Name: %s %s\n", DDS::string_dup(local_user.first_name), DDS::string_dup(local_user.last_name));//i dont know why string_dup makes it work but it does
  wprintw(statusbox, "  Date of Birth: %s", ctime(&temp));
  wprintw(statusbox, "  Highest post count: %i\n", local_user.number_of_highest_post);
  wprintw(statusbox, "  Interest(s): \n");
  for (unsigned int i = 0; i < local_user.interests.length(); i++)
  {
    if (local_user.interests[i])
    wprintw(statusbox, "     %i. %s\n",i+1, DDS::string_dup(local_user.interests[i]));
  }
  wprintw(statusbox, "  Local Posts:\n");
  for (struct response r : local_content)
  {
      wprintw(statusbox, "     Post ID: %i\n", r.post_id);
      wprintw(statusbox, "     Content: %s\n", DDS::string_dup(r.post_body));
      temp = r.date_of_creation;
      wprintw(statusbox, "     Date:    %s\n\n", ctime(&temp));
  }
  makeboxstatus();
  wrefresh(statusbox);
}

//GUI menu to edit current user information
void edit_user_menu(WINDOW *menu_win, user_information target, int highlight)
{
  //number of choices = 7
  //unsigned int i;
  box(menu_win, 0, 0);


  std::time_t temp = target.date_of_birth;
  werase(menu_win);     //clear the window
  mvwprintw(menu_win, 2, 1, "What do you wish to change? (press enter to select)\n");
  if(highlight == 1)
  {
    wattron(menu_win, A_REVERSE);
    wprintw(menu_win, "    UUID: %s\n",target.uuid);
    wattroff(menu_win, A_REVERSE);
  }else
  {
    wprintw(menu_win, "    UUID: %s\n",target.uuid);
  }

  if(highlight == 2)
  {
    wattron(menu_win, A_REVERSE);
    wprintw(menu_win, "    First Name: %s \n", DDS::string_dup(target.first_name));//i dont know why string_dup makes it work but it does
    wattroff(menu_win, A_REVERSE);
  }else
  {
    wprintw(menu_win, "    First Name: %s \n", DDS::string_dup(target.first_name));//i dont know why string_dup makes it work but it does
  }

  if(highlight == 3)
  {
    wattron(menu_win, A_REVERSE);
    wprintw(menu_win, "    Last Name : %s \n", DDS::string_dup(target.last_name));//i dont know why string_dup makes it work but it does
    wattroff(menu_win, A_REVERSE);
  }else
  {
    wprintw(menu_win, "    Last Name : %s \n", DDS::string_dup(target.last_name));//i dont know why string_dup makes it work but it does
  }


  if(highlight == 4)
  {
    wattron(menu_win, A_REVERSE);
    wprintw(menu_win, "    Date of Birth: %s\n", ctime(&temp));
    wattroff(menu_win, A_REVERSE);
  }else
  {
    wprintw(menu_win, "    Date of Birth: %s\n", ctime(&temp));
  }

  if(highlight == 5)
  {
    wattron(menu_win, A_REVERSE);
    wprintw(menu_win, "    Highest post count: %i\n", target.number_of_highest_post);
    wattroff(menu_win, A_REVERSE);
  }else
  {
    wprintw(menu_win, "    Highest post count: %i\n", target.number_of_highest_post);
  }

  if(highlight == 6)
  {
    wattron(menu_win, A_REVERSE);
    wprintw(menu_win, "    Interest(s): \n");
    wattroff(menu_win, A_REVERSE);
  }else
  {
    wprintw(menu_win, "    Interest(s): \n");
  }

  for (unsigned int i = 0; i < target.interests.length(); i++)
  {
    wprintw(menu_win, "       %i. %s\n",i+1, DDS::string_dup(target.interests[i]));
  }

  if(highlight == 7)
  {
    wattron(menu_win, A_REVERSE);
    wprintw(menu_win, "  Exit\n");
    wattroff(menu_win, A_REVERSE);
  }else
  {
    wprintw(menu_win, "  Exit\n");
  }

  box(menu_win, 0, 0);
  wrefresh(menu_win);
}

//helper function to call on edit user
void edit_user(WINDOW *menu_win)
{
  int n_choices = 7;
  //int choice = 1;
  string str;

  int c;
  int exit = 0;

  int highlight = 1;

  keypad(statusbox, TRUE);

  werase(menu_win);     //clear the window
  edit_user_menu(menu_win, local_user, highlight);

  while (exit == 0)
  {
    c = wgetch(menu_win);
    int choice = 0;
    switch(c)
    {
      case KEY_UP:
        if(highlight == 1)
          highlight = n_choices;
        else
          --highlight;
        break;
      case KEY_DOWN:
        if(highlight == n_choices)
          highlight = 1;
        else
          ++highlight;
        break;
      case 10:
        choice = highlight;
        switch(choice)
        {
          case 1:
          {
            //do nothing
          }
            break;
          case 2:
          {
            mvwprintw(menu_win,4  , 16,"                               ");
            wmove(menu_win, 4, 16);
            str = getstringw(menu_win);
            local_user.first_name = DDS::string_dup(str.c_str());
          }
            break;

          case 3:
          {
            mvwprintw(menu_win,5  , 15,"                               ");
            wmove(menu_win, 5, 15);
            str = getstringw(menu_win);
            local_user.last_name = DDS::string_dup(str.c_str());
          }
            break;

          case 4:
          {
            long newdob=0;
            mvwprintw(menu_win,6  , 19,"                               ");
            wmove(menu_win, 6, 19);
            newdob = getintunsignedw(menu_win);
            local_user.date_of_birth = newdob;
          }
            break;
          case 5:
          {
            //do nothing
          }
            break;
          case 6:
          {
            mvwprintw(menu_win, 14, 2,"Would you like to add an Interest or delete one (A/D): ");
            char ad;
            ad = wgetch(menu_win);
            if(ad == 'A' || ad == 'a')
            {
              mvwprintw(menu_win,15, 2,"What interest would you like to add?: ");
              str = getstringw(menu_win);
              local_user.interests.length(local_user.interests.length() + 1);
              local_user.interests[local_user.interests.length()-1] = DDS::string_dup(str.c_str());
            }
            if(ad == 'D' || ad == 'd')
            {
              mvwprintw(menu_win, 15, 2,"What interest number would you like to delete?: ");
              unsigned int rem = getintunsignedw(menu_win);
              vector<string> saved;
              saved.clear();
              for (unsigned int i = 0; i < local_user.interests.length(); i++)
              {
                if (i+1 != rem) saved.push_back(string(local_user.interests[i]));
                else i++;
              }
              local_user.interests.length(local_user.interests.length() - 1);
              int z = 0;
              for (string stack : saved)
              {
                local_user.interests[z] = DDS::string_dup(stack.c_str());
              }
            }
            exit = 1;
          }
            break;
          case 7:
          {
            exit = 1;
          }
          break;

        }
        break;
      default:
        //mvprintw(24, 0, "Charcter pressed is = %3d Hopefully it can be printed as '%c'", c, c);
        refresh();
        break;
    }
    werase(menu_win);
    edit_user_menu(menu_win, local_user, highlight);
  }
}

//primary menu handler, stacked while loop to ensure only one is working at all time
void update_current(int choice)
{
  werase(statusbox);

  switch(choice)
  {
    case 0:
      list_users();
      break;
    case 1:
      show_user_info();
      break;
    case 2:
      post();
      break;
    case 3:
      make_request();
      break;
    case 4:
      network_refresh();
      mvwprintw(statusbox, 1, 1, "Currently available users on the network: %d", filtered_user.size());
      mvwprintw(statusbox, 2, 1, "Currently available content of all user, including local: %d", filtered_response.size() + local_content.size());
      if (local_content.size() == 0) mvwprintw(statusbox, 3, 1, "%% of content owned: %d%%", 0);
      else mvwprintw(statusbox, 3, 1, "%% of content owned: %f%%", (float)local_content.size()/(float)(filtered_response.size() + local_content.size())*100);
      mvwprintw(statusbox, 4, 1, "Refresh completed successfully.");
      break;
    case 5:
      messenger();
      break;
    case 6:
      exited = true;
      exit_procedure();
      break;
    case 7:
      local_information();
      break;
    case 8:
      edit_user(statusbox);
      break;
  }

  box(statusbox, 0, 0);
  wattron(statusbox, A_REVERSE);
  mvwprintw(statusbox, 0, 0, "CURRENT OPERATION");
  wattroff(statusbox, A_REVERSE);
  wrefresh(statusbox);
}

void primary_ui_handler()
{
  //init screen with ncurses
  screen = initscr();
  clear();
  noecho();
  cbreak();
  curs_set(0);

  getmaxyx(screen, maxy, maxx);
  assert(maxy >= RECOMMENDED_WIDTH);
  assert(maxx >= RECOMMENDED_HEIGHT);

  initmenu();
  initchatbox();
  initstatusbox();
  update_menu(0);

  keypad(menubox, TRUE);

  while (!exited)
  {
    int c_menu = wgetch(menubox);
    int current_selection = 0;
    switch(c_menu)
    {
      case KEY_UP:
        if (menu_selection == 0)
          menu_selection = choice_limit-1;
        else
          menu_selection--;
        update_menu(menu_selection);
        break;

      case KEY_DOWN:
        if(menu_selection == choice_limit-1)
          menu_selection = 0;
        else
          menu_selection++;
        update_menu(menu_selection);
        break;

      case 10:
        current_selection = menu_selection;
        update_current(current_selection);
        break;
    }
  }

  endwin();
}

//constantly polling for incoming private messages and display as soon as it arrives
void pull_mail()
{
  while(1)
  {
    message_dump = private_message_sub.recv();
    if (message_dump.size() > 0 && strcmp(message_dump.at(0).sender_uuid, local_user.uuid) != 0)
    {
      werase(chatbox);
      makeboxmessage();
      for (unsigned int i = 0; i < filtered_user.size(); i++)
      {
        if (!strcmp(filtered_user.at(i).uuid, message_dump.at(0).sender_uuid))
          mvwprintw(chatbox, 1, 1, "From: %s %s", DDS::string_dup(filtered_user.at(i).first_name), DDS::string_dup(filtered_user.at(i).last_name));
      }
      mvwprintw(chatbox, 2, 1, "Message: %s",DDS::string_dup(message_dump.at(0).message_body));
      wrefresh(chatbox);
    }
  }
}

#endif
