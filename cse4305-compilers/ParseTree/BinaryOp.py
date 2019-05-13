# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
def binaryResultType( op, lType, rType ) :
  if lType == 'int' and rType == 'int' :
    return 'int'

  return None

def evaluateBinary( op, lValue, rValue ) :
  if op == '+': return lValue + rValue
  elif op == '-': return lValue - rValue
  elif op == '*': return lValue * rValue
  elif op == '/': return lValue / rValue
  elif op == '%': return lValue % rValue
  elif op == '^': return lValue ** rValue
  elif op == '<': return int( lValue < rValue )
  elif op == '<=': return int( lValue <= rValue )
  elif op == '==': return int( lValue == rValue )
  elif op == '>=': return int( lValue >= rValue )
  elif op == '>': return int( lValue > rValue )
  elif op == '!=': return int( lValue != rValue )
  elif op == '&&': return int( lValue and rValue )
  elif op == '||': return int( lValue or rValue )
  return None, 'unknown binary operator'

#---------#---------#---------#---------#---------#--------#
class BinaryOp() :
  def __init__( self, lineNum, op, left, right ) :
    self.m_NodeType = 'BinaryOp'

    self.m_LineNum  = lineNum
    self.m_Op       = op
    self.m_Left     = left
    self.m_Right    = right

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      f'BINARY_OP {self.m_Op!r}', fp )

    self.m_Left.dump( indent+1, fp = fp )
    self.m_Right.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    left = self.m_Left.semantic( symbolTable )
    right = self.m_Right.semantic( symbolTable )

    if left and right:
      typeL = left[2]
      typeR = right[2]
      valueL = left[4]
      valueR = right[4]
      isLitL = left[3]
      isLitR = right[3]

      if binaryResultType( self.m_Op, typeL, typeR ) == 'int' and ( isLitL and isLitR ):
        return ( 'EXPR', ( 'LITERAL', ), typeL, True, evaluateBinary( self.m_Op, int( valueL ), int( valueR ) ) )
      else:
        return ( 'EXPR', ( 'BINARY_OP', self.m_Op, left, right ), typeL, False, None )

#---------#---------#---------#---------#---------#--------#
