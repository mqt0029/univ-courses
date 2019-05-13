# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Statement_Expression() :
  def __init__( self, lineNum, expr ) :
    self.m_NodeType = 'Statement_Expression'

    self.m_LineNum  = lineNum
    self.m_Expr     = expr

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      'STATEMENT (EXPRESSION)', fp )

    self.m_Expr.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    return self.m_Expr.semantic( symbolTable )

#---------#---------#---------#---------#---------#--------#
