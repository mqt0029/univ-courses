NAME: MINH TRAM
STUDENT ID: 1001540029
LANGUAGE: JAVA

CODE STRUCTURE
--------------

Source files includes AiPlayer.java containing all necessary methods for AI class to make the move according
to minimax algorith, GameBoard.java contains all necessary methods to inspect/modify the gameboards, and
maxconnect4.java handles all the initiation, interaction between computer player and human player or game
execution.


EXTRACTION INSTRUCTION
----------------------

After downloading the zipped file from BlackBoard, the extraction command/software should create a folder
named assignment4_mqt0029 with all the necessary files to compile and run the program ( INPUT INCLUDED! )
but feel free to add your input files.


COMPULATION INSTRUCTION
-----------------------

javac *.java

The specified command is all you ever need to run to compile the code.


EXECUTION INSTRUCTION
---------------------

Execution of the program is enforced so that only matching command will be accepted. If parameter is missing,
program WILL NOT RUN, if given input are not found, program WILL NOT RUN. There are 3 possible exec command:

1. java [program name] interactive [input_file] [computer-next / human-next] [depth]
2. java [program name] one-move [input_file] [output_file] [depth]
3. java [program name] debug [ignored] [ignored] [depth] 

Mode 3 is user-specified, can either play with another random or minimax AI. Check debug section in maxconnect4.java
for more details on number of game to play and what mode to play against. If you just call "java maxconnect4", the
same execution instruction will be given.