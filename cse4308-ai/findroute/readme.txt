NAME: MINH TRAM
STUDENT ID: 1001540029
SECTION: CSE4308-001
LANGUAGE: JAVA

CODE STRUCTURE:
  - Class City represents individual city, with enough internal variables to maintain different 
    states of the program as well as built-in functions to handle necessary actions (such as spawning 
    child cities, getting source, etc.)
  - Class Road represents edges connecting between cities, each edge have a duplicate in reverse 
    direction to support bidirectional traversing and internal variable to identify cost and where 
    it is going to
  - Comparable/Comparator functions are customized to fit the need of sorting City and Road, each 
    with their own way of sorting to accommodate for both informed and uninformed search
  - Helper functions (prints, debugs, etc) are also made to assist the program
  - There is advanced usage of for-each loops, bracket shortcuts and scoping

COMPILE AND RUN INSTRUCTIONS:
  1. extract the zipped file, a folder named assignment1_mqt0029 will be created containing the source code, 
     the provided sample input, heuristics file and screenshots of compiling and running the program
  2. Compile using exactly "javac find_route.java", tested on Omega successfully
  3. Execute the program using the specified command line in the format 
     "java find_route <map_input> <from> <to> <heuristics_input>" where
     map_input is the formatted text file to build the map, from is the beginning city, to is the ending city
     and heuristics_input is the heuristic files to be applied. The program will self-adjust between uninformed
     and informed search
  4. CAUTION: the program will do nothing if the number of parameters is incorrect or specified file does not exists,
     double-check the file name if the programs throws any file/input errors.
