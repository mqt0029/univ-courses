# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Statement_While() :
  def __init__( self, lineNum, test, stmt ) :
    self.m_NodeType = 'Statement_While'

    self.m_LineNum  = lineNum
    self.m_TestExpr = test
    self.m_Stmt     = stmt

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      'STATEMENT (WHILE)', fp )

    self.m_TestExpr.dump( indent+1, fp = fp )
    self.m_Stmt.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    test_semantic = self.m_TestExpr.semantic( symbolTable )
    isConstant = test_semantic[3]
    value = test_semantic[4]

    if isConstant:
      if value == 0:
        return ( 'NOOP', )
      else:
        return ( 'LOOP', self.m_Stmt.semantic( symbolTable ) )
    else:
      return ( 'WHILE', test_semantic, self.m_Stmt.semantic( symbolTable ) )

#---------#---------#---------#---------#---------#--------#
