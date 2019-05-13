# Tram, Minh
# mqt0029
# 2019-05-05
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Program() :
  def __init__( self, lineNum, block ) :
    self.m_NodeType = 'Program'

    self.m_LineNum = lineNum
    self.m_Block   = block

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    dumpHeaderLine( indent, self.m_LineNum,
      'PROGRAM', fp )

    self.m_Block.dump( indent+1, fp = fp )

  def semantic( self, symbolTable ) :
    return self.m_Block.semantic( symbolTable )

#---------#---------#---------#---------#---------#--------#
