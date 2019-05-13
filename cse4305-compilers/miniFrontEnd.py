# Tram, Minh
# mqt0029
# 2019-05-05
#---------#---------#---------#---------#---------#--------#
import sys
import traceback

import ply
import ply.yacc
import ply.lex

from pathlib            import Path
from time               import localtime, strftime, time

from AST                import AST
from Exceptions         import *
from ParseTree          import *
from SymbolTable        import SymbolTable

#---------#---------#---------#---------#---------#--------#
lexer  = None
parser = None

#---------#---------#---------#---------#---------#--------#
# Lexical analysis section

reserved = { rw : rw.upper() for rw in (
  'break', 'continue', 'return',
  'if', 'else',
  'read', 'write',
  'while',
  'int', 'float', 'boolean', 'void',
  'array', 'of',
  'func'
  ) }

tokens = [
  'ID', 'INT_LITERAL', 'STRING_LITERAL',
  'ASSIGN',
  'OR',
  'AND',
  'LT', 'LE', 'EQUAL', 'NOTEQUAL',  'GE', 'GT',
  'PLUS', 'MINUS',
  'MULTIPLY', 'DIVIDE', 'MODULUS',
  'EXPONENTIATION',
  'NOT',
  'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN',
  'SEMICOLON', 'COMMA', 'COLON'
  ] + list( reserved.values() )

# Tokens
t_EQUAL     = r'=='

t_AND       = r'&&'
t_COLON     = r':'
t_COMMA     = r','
t_DIVIDE    = r'/'
t_ASSIGN    = r'='
t_EXPONENTIATION = r'\^'
t_GE        = r'>='
t_GT        = r'>'
t_LBRACE    = r'{'
t_LBRACKET  = r'\['
t_LPAREN    = r'\('
t_LE        = r'<='
t_LT        = r'<'
t_MINUS     = r'-'
t_MODULUS   = r'%'
t_MULTIPLY  = r'\*'
t_NOT       = r'!'
t_NOTEQUAL  = r'!='
t_OR        = r'\|\|'
t_PLUS      = r'\+'
t_RBRACE    = r'}'
t_RBRACKET  = r'\]'
t_RPAREN    = r'\)'
t_SEMICOLON = r';'

def t_ID( t ) :
  r'[a-zA-Z_][a-zA-Z0-9_]*'
  t.type = reserved.get( t.value, 'ID' )
  return t

def t_INT_LITERAL( t ) :
  r'\d+'
  t.value = int( t.value )
  return t

def t_STRING_LITERAL( t ) :
  r'"[^"\n]*"'
  t.value = t.value[1:-1]
  return t

#-------------------
# Ignored characters
# Space, formfeed, carriage return, tab, vertical tab
t_ignore = ' \f\r\t\v'

# Eats characters from the // marker to the end of the line.
def t_comment( _ ) :
  r'//[^\n]*'

# Keep track of what line we're on.
def t_newline( t ) :
  r'\n+'
  t.lexer.lineno += t.value.count( '\n' )

#-------------------
def t_error( t ) :
  # Go through elaborate shennanigans to determine the column
  # at which the lexical error occurred.
  lineStart = t.lexer.lexdata.rfind('\n', 0, t.lexer.lexpos) + 1
  column = t.lexer.lexpos - lineStart + 1

  msg = f'Illegal character "{t.value[0]}" at line {t.lexer.lineno}, column {column}.'

  #t.lexer.skip( 1 ) -- We used to just skip the character.
  #                  -- Now we throw an exception.

  raise LexicalError( msg )

#---------#---------#---------#---------#---------#--------#
# Syntactic analysis section

#-------------------
# The start symbol.
start = 'program'

#-------------------
# Precedence rules for the operators
precedence = (
  ( 'right', 'ASSIGN' ),
  ( 'left',  'OR' ),
  ( 'left',  'AND' ),
  ( 'nonassoc', 'EQUAL', 'NOTEQUAL' ),
  ( 'nonassoc',  'LT', 'LE', 'GE', 'GT' ),
  ( 'left',  'PLUS', 'MINUS' ),
  ( 'left',  'MULTIPLY', 'DIVIDE', 'MODULUS' ),
  ( 'right', 'EXPONENTIATION' ),
  ( 'right', 'NOT', 'UMINUS', 'UPLUS' ),
  ( 'left',  'FUNCCALL' )
  )

#-------------------
# PROGRAM ...

def p_program( p ) :
  'program : statement_block'
  p[0] = Program( p.lineno( 1 ), p[1] )

def p_semicolon_opt( p ) :
  '''semicolon_opt : epsilon
                   | SEMICOLON'''

#-------------------
# DECLARATIONS ...
def p_declaration_var( p ) :
  'declaration : ID COLON type init_opt'
  p[0] = Declaration( p.lineno(1), 'VARIABLE', ( p[1], p[3], p[4] ) )

def p_init_opt( p ) :
  '''init_opt : epsilon
              | ASSIGN expression'''
  if p[1] is None :
    p[0] = None

  else :
    p[0] = p[2]

def p_declaration_func( p ) :
  'declaration : FUNC ID LPAREN formal_list_opt RPAREN COLON type statement_block'
  p[0] = Declaration( p.lineno(1), 'FUNCTION', ( p[2], p[4], p[7], p[8] ) )

def p_formal( p ) :
  'formal : ID COLON type'
  p[0] = ( p.lineno(1), p[1], p[3] )

def p_formal_list_opt( p ) :
  '''formal_list_opt : epsilon
                     | formal_list_more formal'''
  if p[1] is None :
    p[0] = []

  else :
    p[1].append( p[2] )
    p[0] = p[1]

def p_formal_list_more( p ) :
  '''formal_list_more : epsilon
                      | formal_list_more formal COMMA'''
  if p[1] is None :
    p[0] = []

  else :
    p[1].append( p[2] )
    p[0] = p[1]

#-------------------
# TYPES ...

# Array type
def p_type_array( p ) :
  'type : ARRAY LBRACKET expression_list_opt RBRACKET OF type'
  p[0] = Type( p.lineno(1), 'ARRAY', ( p[3], p[6] ) )

# Scalar type name
def p_type_name( p ) :
  '''type : INT
          | FLOAT
          | BOOLEAN
          | VOID'''
  p[0] = Type( p.lineno(1), 'NAME', ( p[1], ) )

#-------------------
# STATEMENTS ...

# Block statement
def p_statement_block_A( p ) :
  'statement : statement_block'
  p[0] = p[1]

def p_statement_block_B( p ) :
  'statement_block : LBRACE statement_declaration_list_opt RBRACE'
  p[0] = Statement_Block( p.lineno(1), p[2] )

# Break statement
def p_statement_break( p ) :
  'statement : BREAK'
  p[0] = Statement_Break( p.lineno(1) )

# Continue statement
def p_statement_continue( p ) :
  'statement : CONTINUE'
  p[0] = Statement_Continue( p.lineno(1) )

# Expression statement
def p_statement_expr( p ) :
  'statement : expression'
  p[0] = Statement_Expression( p.lineno(1), p[1] )

# If statement
def p_statement_if(  p ) :
  'statement : IF expression statement_block else_opt'
  p[0] = Statement_If( p.lineno(1), p[2], p[3], p[4] )

def p_else_opt( p ) :
  """else_opt : ELSE statement_block
              | epsilon"""
  p[0] = None if p[1] is None else p[2]

# Read statement
def p_statement_read( p ) :
  'statement : READ LPAREN lvalue_list RPAREN'
  p[0] = Statement_Read( p.lineno(1), p[3] )

# Return statement
def p_statement_return( p ) :
  'statement : RETURN expression_opt'
  p[0] = Statement_Return( p.lineno(1), p[2] )

# Statement / declaration list (statements and declarations
# separated by semicolons).  Possibly zero items in list.
def p_statement_declaration_list_opt( p ) :
  '''statement_declaration_list_opt : epsilon
                                    | statement_declaration_more statement_declaration semicolon_opt'''
  if p[1] is None :
    p[0] = []

  else :
    p[1].append( p[2] )
    p[0] = p[1]

def p_statement_declaration_more( p ) :
  '''statement_declaration_more : epsilon
                                | statement_declaration_more statement_declaration SEMICOLON'''
  if p[1] is None :
    p[0] = []

  else :
    p[1].append( p[2] )
    p[0] = p[1]

def p_statement_declaration( p ) :
  '''statement_declaration : statement
                           | declaration'''
  p[0] = p[1]

# While statement
def p_statement_while( p ) :
  'statement : WHILE expression statement_block'
  p[0] = Statement_While( p.lineno(1), p[2], p[3] )

# Write statement
def p_statement_write( p ) :
  'statement : WRITE LPAREN expression_list_opt RPAREN'
  p[0] = Statement_Write( p.lineno(1), p[3] )

#-------------------
# LVALUES ...

def p_lvalue_ID( p ) :
  'lvalue : ID'
  p[0] = Lvalue( p.lineno(1), 'NAME', ( p[1], ) )

def p_lvalue_ArrayRef( p ) :
  'lvalue : lvalue LBRACKET expression_list_opt RBRACKET'
  p[0] = Lvalue( p.lineno(1), 'ARRAYREF', ( p[1], p[3] ) )

def p_lvalue_list_A( p ) :
  'lvalue_list : lvalue_list COMMA lvalue'
  p[1].append( p[3] )
  p[0] = p[1]

def p_lvalue_list_B( p ) :
  'lvalue_list : lvalue'
  p[0] = [ p[1] ]

#-------------------
# EXPRESSIONS ...

# Binary operator expression
def p_expression_binop( p ) :
  '''expression : expression PLUS     expression
                | expression MINUS    expression
                | expression MULTIPLY expression
                | expression DIVIDE   expression
                | expression MODULUS  expression
                | expression EXPONENTIATION expression
                | expression LT       expression
                | expression LE       expression
                | expression EQUAL    expression
                | expression NOTEQUAL expression
                | expression GE       expression
                | expression GT       expression
                | expression AND      expression
                | expression OR       expression
                | lvalue     ASSIGN   expression'''
  p[0] = BinaryOp( p.lineno(2), p[2], p[1], p[3] )

# Unary operator expression
def p_expression_unop( p ) :
  '''expression : MINUS expression %prec UMINUS
                | PLUS  expression %prec UPLUS
                | NOT   expression'''
  p[0] = UnaryOp( p.lineno(1), p[1], p[2] )

# Parenthesized expression
def p_expression_group( p ) :
  'expression : LPAREN expression RPAREN'
  p[0] = p[2]

# Integer literal
def p_expression_int_literal( p ) :
  'expression : INT_LITERAL'
  p[0] = Literal( p.lineno( 1 ), 'int', p[1] )

# String literal
def p_expression_str_literal( p ) :
  'expression : STRING_LITERAL'
  p[0] = Literal( p.lineno( 1 ), 'string', p[1] )

# Lvalue
def p_expression_lvalue( p ) :
  'expression : lvalue'
  p[0] = p[1]

# Function call
def p_expression_funccall( p ) :
  'expression : ID LPAREN expression_list_opt RPAREN %prec FUNCCALL'
  p[0] = FuncCall( p.lineno(1), p[1], p[3] )

# Expression list (expressions separated by commas).
# Might be zero expression in the list.
def p_expression_list_opt( p ) :
  '''expression_list_opt : epsilon
                         | expression_list_more expression'''
  if p[1] is None :
    p[0] = []

  else :
    p[1].append( p[2] )
    p[0] = p[1]

def p_expression_list_more( p ) :
  '''expression_list_more : epsilon
                          | expression_list_more expression COMMA'''
  if p[1] is None :
    p[0] = []

  else :
    p[1].append( p[2] )
    p[0] = p[1]

def p_expression_opt( p ) :
  '''expression_opt : expression
                    | epsilon'''
  p[0] = p[1]

#-------------------
# The 'empty' value.  It's possible to just have an empty RHS
# in a production, but having the non-terminal 'epsilon' makes
# it much more obvious that the empty string is being parsed.
def p_epsilon( p ) :
  'epsilon :'
  p[0] = None

#-------------------
# Gets called if an unexpected token (or the EOF) is seen during
# a parse.  We throw an exception
def p_error( p ) :
  msg = 'Syntax error at '
  if p is None :
    msg += 'EOF.'

  else :
    # Go through elaborate shennanigans to determine the column
    # at which the parse error occurred.
    lineStart = lexer.lexdata.rfind('\n', 0, p.lexpos) + 1
    column = p.lexpos - lineStart + 1

    msg += f'token "{p.value}", line {p.lineno}, column {column}'

  raise SyntacticError( msg )

#---------#---------#---------#---------#---------#--------#
def _main( inputFileName ) :
  global lexer
  global parser

  begin = time()
  timestamp = strftime( '%Y-%m-%d %H:%M:%S', localtime( begin ) )

  fileName  = str( Path( inputFileName ).name )
  parseFile = str( Path( inputFileName ).with_suffix( '.parse' ) )
  astFile   = str( Path( inputFileName ).with_suffix( '.ast' ) )

  print( f'#----------\n# Begin at {timestamp}' )
  print( f'# Reading source file {inputFileName!r} ...' )

  strt = time()
  with open( inputFileName, 'r' ) as fp :
    data = fp.read()

  print( f'#    Read succeeded.  ({time()-strt:.3f}s)' )
  print( f'# Beginning parse ...' )

  try :
    strt    = time()
    lexer   = ply.lex.lex()
    parser  = ply.yacc.yacc()
    program = parser.parse( data, tracking = True )

    print( f'#    Parse succeeded.  ({time()-strt:.3f}s)' )
    print( f'# Beginning parse tree dump to {parseFile!r} ...' )

    strt = time()
    with open( parseFile, 'w' ) as fp :
      print( f'# {fileName} parse tree\n# {timestamp}\n\n', file = fp )
      program.dump( fp = fp )

    print( f'#    Parse dumped.  ({time()-strt:.3f}s)' )
    print( f'# Beginning semantic analysis ...' )

    strt = time()
    symbolTable = SymbolTable()
    ast = program.semantic( symbolTable )

    print( f'#   Semantic analysis complete.  ({time()-strt:.3f}s)' )
    print( f'# Beginning AST/Symbol Table dump to {astFile!r} ...' )

    strt = time()
    with open( astFile, 'w' ) as fp :
      print( f'# {fileName} AST\n# {timestamp}\n\n', file = fp )
      AST().dump( ast, fp = fp )

      print( f'\n\n# {fileName} symbol table\n# {timestamp}\n\n', file = fp )
      symbolTable.dump( fp = fp )

    print( f'#   AST/Symbol Table dumped.  ({time()-strt:.3f}s)' )

    finish = time()
    total = finish - begin
    timestamp = strftime( '%Y-%m-%d %H:%M:%S', localtime( finish ) )
    print( f'# End at {timestamp}' )
    print( f'# Total time {total:.3f}s.\n#----------')

  except ( LexicalError, SyntacticError, SemanticError, InternalError ) as e :
    #print( 'Exception detected analysis.' )
    print( e )
    #traceback.print_exc()
    sys.exit( 1 )

  except :
    print( '*** (Unknown) exception detected during parse/result dump.' )
    traceback.print_exc()
    sys.exit( 1 )

#---------#---------#---------#
if __name__ == '__main__' :
  if len( sys.argv ) > 1 :
    _main( sys.argv[ 1 ] )

  else :
    print( 'Input file name required.' )

#---------#---------#---------#---------#---------#--------#
