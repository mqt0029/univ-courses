# Tram, Minh
# mqt0029
# 2019-05-05
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *

#---------#---------#---------#---------#---------#--------#
class Type() :
  def __init__( self, lineNum, kind, args ) :
    self.m_NodeType = 'Type'

    self.m_LineNum = lineNum
    self.m_Kind    = kind
    self.m_Args    = args

  def __repr__( self ) :
    if self.m_Kind == 'NAME' :
      return f'TYPE (NAME) {self.m_Args[0]!r}'

    elif self.m_Kind == 'ARRAY' :
      return f'TYPE (ARRAY) <{len(self.m_Args[0])}>'

    else :
      return f'TYPE ({self.m_Kind!r}) unknown'

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    if self.m_Kind == 'NAME' :
      dumpHeaderLine( indent, self.m_LineNum,
        f'TYPE (NAME) {self.m_Args[0]!r}', fp )

    elif self.m_Kind == 'ARRAY' :
      dumpHeaderLine( indent, self.m_LineNum,
        f'TYPE (ARRAY) <{len(self.m_Args[0])}>', fp )

      for e in self.m_Args[0] :
        e.dump( indent+1, fp = fp )

      self.m_Args[1].dump( indent+1, fp = fp )

    else :
      dumpHeaderLine( indent, self.m_LineNum,
        f'TYPE ({self.m_Kind!r}) unknown', fp )

  def semantic( self, symbolTable ) :
    return self.m_Args[0]

#---------#---------#---------#---------#---------#--------#
