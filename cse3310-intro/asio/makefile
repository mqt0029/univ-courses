CXX=g++
CXXFLAGS=-I./include -Wall -O0 -g -std=c++11

all: chat_server chat_client

chat_client: chat_client.cpp
	${CXX} -o $@ ${CXXFLAGS} $^ -lpthread -lncurses

chat_server: chat_server.cpp
	${CXX} -o $@ ${CXXFLAGS} $^ -lpthread -lncurses

clean:
	-rm -rf chat_client chat_server chat_client.o chat_server.o chat_client.dSYm chat_server.dSYM

