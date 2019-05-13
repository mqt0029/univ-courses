#-------------------------------------------------------------------------------
# Student Name: Minh Tram
# Student ID: 1001540029
# Section: CSE4308-001
# Name:        check_true_false
# Purpose:     Main entry into logic program. Reads input files, creates 
#              base, tests statement, and generates result file.
#-------------------------------------------------------------------------------

import sys
from logical_expression import *

def main(argv):

    original_model = {}

    if len(argv) != 4:
        print('Usage: %s [wumpus-rules-file] [additional-knowledge-file] [input_file]' % argv[0])
        sys.exit(0)

    # Read wumpus rules file
    try:
        input_file = open(argv[1], 'rb')
    except:
        print('failed to open file %s' % argv[1])
        sys.exit(0)

    # Create the knowledge base with wumpus rules
    print '\nLoading wumpus rules...',
    knowledge_base = logical_expression()
    knowledge_base.connective = ['and']
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # A mutable counter so recursive calls don't just make a copy
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)
    input_file.close()
    print 'done.'

    # Read additional knowledge base information file
    try:
        input_file = open(argv[2], 'rb')
    except:
        print('failed to open file %s' % argv[2])
        sys.exit(0)

    # Add expressions to knowledge base
    print 'Loading additional knowledge...',
    for line in input_file:
        # Skip comments and blank lines. Consider all line ending types.
        if line[0] == '#' or line == '\r\n' or line == '\n' or line == '\r':
            continue
        counter = [0]  # a mutable counter
        subexpression = read_expression(line.rstrip('\r\n'), counter)
        knowledge_base.subexpressions.append(subexpression)

        if subexpression.symbol[0]:
          original_model[ subexpression.symbol[0] ] = True
        else:
          original_model[ subexpression.subexpressions[0].symbol[0] ] = False
          
    input_file.close()
    print 'done.'

    # Verify it is a valid logical expression
    if not valid_expression(knowledge_base):
        sys.exit('invalid knowledge base')

    # Read statement whose entailment we want to determine
    try:
        input_file = open(argv[3], 'rb')
    except:
        print('failed to open file %s' % argv[3])
        sys.exit(0)
    print 'Loading statement...',
    statement = input_file.readline().rstrip('\r\n')
    input_file.close()
    print 'done.'
    
    # Convert statement into a logical expression and verify it is valid
    statement = read_expression(statement)
    if not valid_expression(statement):
        sys.exit('invalid statement')

    # Show us what the statement is
    print '\nChecking statement: ',
    print_expression(statement, '')
    print ' is valid.'

    # Run the statement through the inference engine
    result = check_true_false( knowledge_base, statement, original_model )
    print 'Result = ' + result

    sys.exit(1)
    

if __name__ == '__main__':
    main(sys.argv)
