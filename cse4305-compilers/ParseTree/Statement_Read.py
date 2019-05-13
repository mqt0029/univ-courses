# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Statement_Read() :
  def __init__( self, lineNum, idList ) :
    self.m_NodeType = 'Statement_Read'

    self.m_LineNum = lineNum
    self.m_IDList  = idList

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      f'STATEMENT (READ) <{len(self.m_IDList)}>', fp )

    for lvalue in self.m_IDList :
      lvalue.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    return ( 'READ', [ lval.semantic( symbolTable ) for lval in self.m_IDList ] )

#---------#---------#---------#---------#---------#--------#
