# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *
from .Exceptions   import SemanticError

#---------#---------#---------#---------#---------#--------#
class Lvalue() :
  def __init__( self, lineNum, kind, args ) :
    self.m_NodeType = 'Lvalue'

    self.m_LineNum = lineNum
    self.m_Kind    = kind
    self.m_Args    = args

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    if self.m_Kind == 'NAME' :
      dumpHeaderLine( indent, self.m_LineNum,
        f'LVALUE (NAME) {self.m_Args[0]!r}', fp )

    elif self.m_Kind == 'ARRAYREF' :
      dumpHeaderLine( indent, self.m_LineNum,
        f'LVALUE (ARRAYREF) <{len(self.m_Args[1])}>', fp )

      self.m_Args[0].dump( indent+1, fp = fp )

      for e in self.m_Args[1] :
        e.dump( indent+1, fp = fp )

    else :
      dumpHeaderLine( indent, self.m_LineNum,
        f'LVALUE ({self.m_Kind!r}) unknown', fp )

  def semantic( self, symbolTable ) :
    if self.m_Kind != 'NAME':
      raise SemanticError( f'({self.m_LineNum}) Non-name lvalue encountered.' )
    
    name = self.m_Args[0]
    entry = symbolTable.findName( name )

    if entry is None:
      raise SemanticError( f'({self.m_LineNum}) Undeclared name {name!r} encountered.' )

    return ( 'EXPR', ( 'LVALUE', entry.qualifiedName ), entry.myType, False, None )

#---------#---------#---------#---------#---------#--------#
