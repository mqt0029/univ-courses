#ifndef TSNCOMMUNICATION_H
#define TSNCOMMUNICATION_H

#include "tsnHeader.h"
#include "tsnGlobalVars.h"

//clear local storage after startup
void init_storage()
{
  //verify empty vectors
  userinfo_dump.clear();
  response_dump.clear();
  request_dump.clear();
  floating_dump.clear();
  filtered_user.clear();
  filtered_response.clear();
  filtered_request.clear();
  filtered_floating.clear();

  filtered_user.push_back(local_user);
}

//initial network content pulled
void init_network_content()
{
  userinfo_dump = userinf_sub.recv();
  response_dump = response_sub.recv();
  floating_dump = response_sub.recv();
  request_dump = request_sub.recv();
}

//initial local content read from locally hidden files
//make default if file not found
void init_local_content()
{
  ifstream source_user(local_user_data);
  if (source_user.is_open())
  {
    string temp; int limit = 0;
    source_user.seekg(0,ios_base::beg);
    source_user >> local_user.uuid;
    source_user >> local_user.date_of_birth;
    source_user >> temp;
    local_user.first_name = DDS::string_dup(temp.c_str());
    source_user >> temp;
    local_user.last_name = DDS::string_dup(temp.c_str());
    source_user >> local_user.number_of_highest_post;
    source_user >> limit;
    local_user.interests.length(limit);
    for (int i = 0; i < limit; i++)
    {
      source_user >> temp;
      local_user.interests[i] = DDS::string_dup(temp.c_str());
    }
    source_user.close();
  }
  else
  {
    ofstream destination_user(local_user_data, ofstream::trunc);
    destination_user.seekp(ios_base::beg);
    boost::uuids::uuid uuid = boost::uuids::random_generator()();
    strncpy(local_user.uuid, boost::uuids::to_string(uuid).c_str(),sizeof(local_user.uuid));
    local_user.uuid[sizeof(local_user.uuid)-1] = '\0';
    local_user.date_of_birth = 1;
    local_user.first_name = "John";
    local_user.last_name = "Doe";
    local_user.interests.length(2);
    local_user.interests[0] = DDS::string_dup("C");
    local_user.interests[1] = DDS::string_dup("C++");
    local_user.number_of_highest_post = 0;
    destination_user << local_user.uuid << endl;
    destination_user << local_user.date_of_birth << endl;
    destination_user << local_user.first_name << endl;
    destination_user << local_user.last_name << endl;
    destination_user << local_user.number_of_highest_post << endl;
    destination_user << local_user.interests.length() << endl;
    for (unsigned int i = 0; i < local_user.interests.length(); i++)
    {
      destination_user << local_user.interests[i] << endl;
    }
    destination_user.close();
  }

  ifstream source_content(local_content_data);
  if (source_content.is_open()) //local content found
  {
    int limit;
    source_content >> limit;
    source_content.ignore();
    for (int a = 0; a < limit; a++)
    {
      //increment serial numbers
      local_serial_number++;

      //helper variables
      response stacker;
      string uuid, body;
      int pid, create, parent_metadata, child_metadata;

      /* grabbing post content */

      //getting uuid
      getline(source_content,uuid);
      source_content >> pid;
      source_content.ignore();

      //get post body
      getline(source_content,body);

      //get post time stamp
      source_content >> create;

      source_content.ignore();

      //assign to structure
      strncpy(stacker.uuid, uuid.c_str(),sizeof(stacker.uuid));
      stacker.uuid[sizeof(stacker.uuid)-1] = '\0';
      stacker.post_id = pid;
      stacker.post_body = DDS::string_dup(body.c_str());
      stacker.date_of_creation = create;

      source_content >> parent_metadata;
      source_content.ignore();
      source_content >> child_metadata;
      source_content.ignore();

      if (parent_metadata)
      {
        string parent_uuid;
        int parent_serial;
        getline(source_content, parent_uuid);

        source_content >> parent_serial;
        source_content.ignore();

        strncpy(stacker.parent_post.owner_uuid, parent_uuid.c_str(), sizeof(stacker.parent_post.owner_uuid));
        stacker.parent_post.owner_uuid[sizeof(stacker.parent_post.owner_uuid)-1] = '\0';
        stacker.parent_post.post_id = parent_serial;
      }
      else
      {
        memset(stacker.parent_post.owner_uuid, '0', sizeof(stacker.parent_post.owner_uuid));
        stacker.parent_post.owner_uuid[sizeof(stacker.parent_post.owner_uuid)-1] = '\0';
        stacker.parent_post.post_id = 0;
      }

      if (child_metadata)
      {
        int count;

        source_content >> count;
        source_content.ignore();

        stacker.child_posts.length(count);
        for (int i = 0; i < count; i++)
        {
          string child_uuid;
          int child_serial;
          getline(source_content, child_uuid);

          source_content >> child_serial;
          source_content.ignore();

          strncpy(stacker.child_posts[i].owner_uuid, child_uuid.c_str(), sizeof(stacker.child_posts[i].owner_uuid));
          stacker.child_posts[i].owner_uuid[sizeof(stacker.child_posts[i].owner_uuid)-1] = '\0';
          stacker.child_posts[i].post_id = child_serial;
        }
      }
      else
      {
        stacker.child_posts.length(0);
      }

      //append post to array
      local_content.push_back(stacker);

      source_content.ignore();
    }
    source_content.close();
  }
  else  //local content not found
  {
    ofstream destination_content(local_content_data, ofstream::trunc);
    int count = 0;
    destination_content << count;
    destination_content.close();
  }
}

//refresh network content, repulling everything that's currently available on the network
void network_refresh()
{
  init_storage();
  init_network_content();

  userinf_pub.publish(local_user);

  if (userinfo_dump.size() > 0)
  {
    if (filtered_user.size() == 0) filtered_user.push_back(userinfo_dump.at(0));

    for (struct user_information target : userinfo_dump)
    {
      bool existed = false;

      for (struct user_information compare : filtered_user)
        if (!strcmp(compare.uuid, target.uuid)) existed = !existed;

      if (!existed) filtered_user.push_back(target);
    }
  }
  else {} //do nothing

  if (response_dump.size() > 0)
  {
    if (filtered_response.size() == 0) filtered_response.push_back(response_dump.at(0));

    for (struct response target : response_dump)
    {
      bool existed = false;
      for (struct response compare : filtered_response)
        if (!strcmp(target.uuid, compare.uuid) && (target.post_id == compare.post_id)) existed = !existed;

      if (!existed) filtered_response.push_back(target);
    }
  }
  else {} //do nothing

  if (request_dump.size() > 0)
  {
    if (filtered_request.size() == 0) filtered_request.push_back(request_dump.at(0));

    for (struct request target : request_dump)
    {
      bool existed = false;
      for (struct request compare : filtered_request)
      {
        if (!strcmp(compare.uuid, target.uuid)) existed = !existed;
      }

      if (!existed) filtered_request.push_back(target);
    }
  }
  else {}
}

//shortcut to init/reinit system
void init_system()
{
  init_storage();
  init_local_content();
  init_network_content();
  sleep(1);
  network_refresh();
}

//background publisher, to make sure this node is visible on the network at all time
void background_publisher()
{
  while(1)
  {
    userinf_pub.publish(local_user);
    if (timelapse_counter == 2 && request_available == false)
    {
      request_available = true;
      timelapse_counter = 0;
      network_refresh();
    }
    sleep(30);
    timelapse_counter++;
  }
}

//responding to any incoming requests that matches local content. Work once, don't know why it doesn't loop.
void request_handler()
{
  //Response publisher, don't have a mean to test yet. Should work since exact same working principle with Request publisher
  //TODO: make stalker send acceptable request and see if a response is received on stalker end
  while(1)
  {
    while(filtered_request.size() <= 0) request_sub.recv();

    //scan through available request, need REFRESH() to make sure not sending info for dead requests
    for (unsigned int i = 0; i < filtered_request.size(); i++)
    {
      //scan through sub-sequence of node requests vector
      for (unsigned int j = 0; j < filtered_request[i].user_requests.length(); j++)
      {
        //check if any fulfiller uuid matches ours local id. If yes, go look in local content for potential response
        if (!strcmp(filtered_request[i].user_requests[j].fulfiller_uuid,local_user.uuid))
        {
          //scan through list of requested content, search by serial number
          for (unsigned int k = 0; k < filtered_request[i].user_requests[j].requested_posts.length();k++)
          {
            //ensure it cannot go out of bound of the local vector
            for (unsigned int l = 0; l < local_content.size(); l++)
            {
              //if reached here, means there are content that we owned locally need to be published as response
              if (filtered_request[i].user_requests[j].requested_posts[k] == local_content[l].post_id)
              {
                //send out requested reponse, limit to 1 respond/sec per requirement
                response_pub.publish(local_content[l]);
                sleep(1);
              }
            }
          }
        }
      }
    }
    filtered_request.clear();
  }
}

#endif
