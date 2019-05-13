#-------------------------------------------------------------------------------
# Student Name: Minh Tram
# Student ID: 1001540029
# Section: CSE4308-001
# Name:        logical_expression
# Purpose:     Contains logical_expression class, inference engine,
#              and assorted functions
#-------------------------------------------------------------------------------

import sys
from copy import deepcopy

db = open( 'debug.txt', 'w' )
dbloop = 0

#-------------------------------------------------------------------------------
# Begin code that is ported from code provided by Dr. Athitsos
class logical_expression:
    """A logical statement/sentence/expression class"""
    # All types need to be mutable, so we don't have to pass in the whole class.
    # We can just pass, for example, the symbol variable to a function, and the
    # function's changes will actually alter the class variable. Thus, lists.
    def __init__(self):
        self.symbol = ['']
        self.connective = ['']
        self.subexpressions = []


def print_expression(expression, separator):
  """Prints the given expression using the given separator"""
  if expression == 0 or expression == None or expression == '':
      print '\nINVALID\n'

  elif expression.symbol[0]: # If it is a base case (symbol)
      sys.stdout.write('%s' % expression.symbol[0])

  else: # Otherwise it is a subexpression
      sys.stdout.write('(%s' % expression.connective[0])
      for subexpression in expression.subexpressions:
          sys.stdout.write(' ')
          print_expression(subexpression, '')
          sys.stdout.write('%s' % separator)
      sys.stdout.write(')')

def print_expression_file( expr ):
  line = ''
  if expr.symbol[0]:
    line += str( expr.symbol[0] )
  else:
    line += '(' + str( expr.connective[0] )
    for subexpr in expr.subexpressions:
      line += ' '
      line += print_expression_file( subexpr )
  line += ')'
  return line.upper()


def read_expression(input_string, counter=[0]):
    """Reads the next logical expression in input_string"""
    # Note: counter is a list because it needs to be a mutable object so the
    # recursive calls can change it, since we can't pass the address in Python.
    result = logical_expression()
    length = len(input_string)
    while True:
        if counter[0] >= length:
            break

        if input_string[counter[0]] == ' ':    # Skip whitespace
            counter[0] += 1
            continue

        elif input_string[counter[0]] == '(':  # It's the beginning of a connective
            counter[0] += 1
            read_word(input_string, counter, result.connective)
            read_subexpressions(input_string, counter, result.subexpressions)
            break

        else:  # It is a word
            read_word(input_string, counter, result.symbol)
            break
    return result


def read_subexpressions(input_string, counter, subexpressions):
    """Reads a subexpression from input_string"""
    length = len(input_string)
    while True:
        if counter[0] >= length:
            print '\nUnexpected end of input.\n'
            return 0

        if input_string[counter[0]] == ' ':     # Skip whitespace
            counter[0] += 1
            continue

        if input_string[counter[0]] == ')':     # We are done
            counter[0] += 1
            return 1

        else:
            expression = read_expression(input_string, counter)
            subexpressions.append(expression)


def read_word(input_string, counter, target):
    """Reads the next word of an input string and stores it in target"""
    while True:
        if counter[0] >= len(input_string):
            break

        if input_string[counter[0]].isalnum() or input_string[counter[0]] == '_':
            target[0] += input_string[counter[0]]
            counter[0] += 1

        elif input_string[counter[0]] == ')' or input_string[counter[0]] == ' ':
            break

        else:
            print('Unexpected character %s.' % input_string[counter[0]])
            sys.exit(1)


def valid_expression(expression):
    """Determines if the given expression is valid according to our rules"""
    if expression.symbol[0]:
        return valid_symbol(expression.symbol[0])

    if expression.connective[0].lower() == 'if' or expression.connective[0].lower() == 'iff':
        if len(expression.subexpressions) != 2:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() == 'not':
        if len(expression.subexpressions) != 1:
            print('Error: connective "%s" with %d arguments.' %
                        (expression.connective[0], len(expression.subexpressions)))
            return 0

    elif expression.connective[0].lower() != 'and' and \
         expression.connective[0].lower() != 'or' and \
         expression.connective[0].lower() != 'xor':
        print('Error: unknown connective %s.' % expression.connective[0])
        return 0

    for subexpression in expression.subexpressions:
        if not valid_expression(subexpression):
            return 0
    return 1


def valid_symbol(symbol):
    """Returns whether the given symbol is valid according to our rules."""
    if not symbol:
        return 0

    for s in symbol:
        if not s.isalnum() and s != '_':
            return 0
    return 1

# End of ported code
#-------------------------------------------------------------------------------

# Add all your functions here

def check_true_false( KB, alpha, model ):
  global db

  print '\nBeginning evaluation of ',
  print_expression( alpha, '' )
  print '...'

  symbols = []
  symbols.extend( get_symbols( KB ) )
  symbols.extend( get_symbols( alpha ) )
  symbols = list( set( symbols ) )

  for key, value in list( model.items() ):
    symbols.remove( key )
  
  print >> db, '\nWORKING ON KB |= ALPHA'
  print >> db, '========================'

  #evaluate KB entails statement
  result_kb_alpha = tt_entails( KB, alpha, deepcopy( symbols ), deepcopy( model) )
  print 'KB entails alpha     = ' + str(result_kb_alpha)

  #evaluate KB entails NOT statement
  not_alpha = logical_expression()
  not_alpha.connective = ['NOT']
  not_alpha.subexpressions.append( alpha )

  print >> db, '\nWORKING ON KB |= NOT ALPHA'
  print >> db, '========================'

  result_kb_not_alpha = tt_entails( KB, not_alpha, deepcopy( symbols ), deepcopy( model) )
  print 'KB entails NOT alpha = ' + str(result_kb_not_alpha)

  #output file
  file = open( 'result.txt', 'wb' )

  final_string = ''

  if result_kb_alpha == True and result_kb_not_alpha == False:
    final_string = 'definitely true'
  elif result_kb_not_alpha == True and result_kb_alpha == False:
    final_string = 'definitely false'
  elif result_kb_alpha == False and result_kb_not_alpha == False:
    final_string = 'possibly true, possibly false'
  elif result_kb_alpha == True and result_kb_not_alpha == True:
    final_string = 'both true and false'

  print >> file, final_string

  file.close()

  #debug file handler
  db.close()

  #return result_kb
  return final_string

def tt_entails( KB, alpha, symbols, model ):
  #debug stuff
  global db

  print >> db, 'symbol count    = ' + str( len( symbols ) )
  print >> db, 'model count     = ' + str( len( model ) )
  print >> db, 'list of unknown symbols = ' + str( symbols )
  print >> db, 'original model  = ' + str( model )

  return tt_check_all( KB, alpha, symbols, model )


def tt_check_all( KB, alpha, symbols, model ):

  global dbloop, db
  dbloop+=1
  print >> db, '\n'
  print >> db, 'loop = ' + str( dbloop )
  print >> db, 'symbol count = ' + str( len( symbols ) )
  print >> db, 'symbols = ' + str( symbols )
  print >> db, 'before model = ' + str( model )

  if len( symbols ) == 0:
    if pl_true( KB, model ) == True:
      return pl_true( alpha, model )
    else: return True
  else:
    P = symbols.pop(0)
    check_true  = tt_check_all( KB, alpha, deepcopy( symbols ), extend_model( model, P, True ) )
    check_false = tt_check_all( KB, alpha, deepcopy( symbols ), extend_model( model, P, False ) )
    return check_true and check_false


def pl_true( expr, model ):
  if expr.symbol[0]:
    return model[ expr.symbol[0] ]

  elif expr.connective[0].lower() == 'and':
    result = True
    for subexpr in expr.subexpressions:
      result = result and pl_true( subexpr, model )
    return result

  elif expr.connective[0].lower() == 'or':
    result = False
    for subexpr in expr.subexpressions:
      result = result or pl_true( subexpr, model )
    return result

  elif expr.connective[0].lower() == 'xor':
    truecount = 0
    for subexpr in expr.subexpressions:
      if pl_true( subexpr, model ) == True: truecount += 1
    if truecount != 1: return False
    else: return True

  elif expr.connective[0].lower() == 'if':
    if pl_true( expr.subexpressions[0], model ) == True and pl_true( expr.subexpressions[1], model ) == False:
      return False
    return True
    
  elif expr.connective[0].lower() == 'iff':
    if pl_true( expr.subexpressions[0], model ) == pl_true( expr.subexpressions[1], model ):
      return True
    return False
    
  elif expr.connective[0].lower() == 'not':
    return not pl_true( expr.subexpressions[0], model )

def extend_model( model, symbol, value ):
  extended_model = deepcopy( model )
  extended_model[ symbol ] = value

  global db
  print >> db, 'after model = ' + str( extended_model )

  return extended_model

def get_symbols( expr ):
  symbols = []
  if expr.symbol[0]:
    symbols.append( expr.symbol[0] )
  else:
    for subexpr in expr.subexpressions:
      symbols.extend( get_symbols( subexpr ) )
  return symbols