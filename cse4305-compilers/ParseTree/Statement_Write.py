# Tram, Minh
# mqt0029
# 2019-05-05
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Statement_Write() :
  def __init__( self, lineNum, exprList ) :
    self.m_NodeType = 'Statement_Write'

    self.m_LineNum  = lineNum
    self.m_ExprList = exprList

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      f'STATEMENT (WRITE) <{len(self.m_ExprList)}>', fp )

    for e in self.m_ExprList :
      e.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    return ( 'WRITE', [ expr.semantic( symbolTable ) for expr in self.m_ExprList ] )

#---------#---------#---------#---------#---------#--------#
