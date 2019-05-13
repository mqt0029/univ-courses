# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Statement_If() :
  def __init__( self, lineNum, test, thenStmt, elseStmt ) :
    self.m_NodeType = 'Statement_If'

    self.m_LineNum  = lineNum
    self.m_TestExpr = test
    self.m_ThenStmt = thenStmt
    self.m_ElseStmt = elseStmt

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    if self.m_ElseStmt is None :
      hdrStr = 'STATEMENT (IF-THEN)'

    else :
      hdrStr = 'STATEMENT (IF-THEN-ELSE)'

    dumpHeaderLine( indent, self.m_LineNum,
      hdrStr, fp )

    self.m_TestExpr.dump( indent+1, fp = fp )
    self.m_ThenStmt.dump( indent+1, fp = fp )
    if self.m_ElseStmt is not None :
      self.m_ElseStmt.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    test_semantic = self.m_TestExpr.semantic( symbolTable )
    isConstant = test_semantic[3]
    value = test_semantic[4]

    if self.m_ElseStmt:
      if isConstant:
        if value == 0:
          return self.m_ElseStmt.semantic( symbolTable )
        else:
          return self.m_ThenStmt.semantic( symbolTable )
      else:
        return ( 'IF', test_semantic, self.m_ThenStmt.semantic( symbolTable ), self.m_ElseStmt.semantic( symbolTable ) )
    else:
      if isConstant:
        if value == 0:
          return ( 'NOOP', )
        else:
          return self.m_ThenStmt.semantic( symbolTable )
      else:
        return ( 'IF', test_semantic, self.m_ThenStmt.semantic( symbolTable ), ( 'NOOP', ) )         

#---------#---------#---------#---------#---------#--------#
