# Tram, Minh
# mqt0029
# 2019-05-05
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
def unaryResultType( op, rType ) :
  if rType == 'int':
    return 'int'

  return None

def evaluateUnary( op, rValue ) :
  if op == '+': return rValue + 1
  elif op == '-': return -1 * rValue
  elif op == '!': return not rValue
  return None, 'unknown unary operator'

#---------#---------#---------#---------#---------#--------#
class UnaryOp() :
  def __init__( self, lineNum, op, right ) :
    self.m_NodeType = 'UnaryOp'

    self.m_LineNum  = lineNum
    self.m_Op       = op
    self.m_Right    = right

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      f'UNARY_OP {self.m_Op!r}', fp )

    self.m_Right.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    right = self.m_Right.semantic( symbolTable )

    if right:
      typeR = right[2]
      valueR = right[4]
      isLitR = right[3]

      if unaryResultType( self.m_Op, typeR ) and isLitR:
        return ( 'EXPR', ( 'LITERAL', ), typeR, True, evaluateUnary( self.m_Op, valueR ) )
      else:
        return ( 'EXPR', ( 'UNARY_OP', self.m_Op, right ), typeR, False, None )

#---------#---------#---------#---------#---------#--------#
