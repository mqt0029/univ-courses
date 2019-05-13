# Tram, Minh
# mqt0029
# 2019-05-05
#---------#---------#---------#---------#---------#--------#
import sys

from .common       import *
from .Exceptions   import SemanticError

#---------#---------#---------#---------#---------#--------#
DEFAULT_VALUE = {
  'boolean' : False,
  'float'   : 0.0,
  'int'     : 0,
  'string'  : ''
}

#---------#---------#---------#---------#---------#--------#
class Declaration() :
  def __init__( self, lineNum, kind, args ) :
    self.m_NodeType = 'Declaration'

    self.m_LineNum = lineNum
    self.m_Kind    = kind
    self.m_Args    = args

  #---------------------------------------
  def dump( self, indent = 0, fp = sys.stdout ) :
    if self.m_Kind == 'VARIABLE' :
      init = self.m_Args[2]

      if init is None :
        dumpHeaderLine( indent, self.m_LineNum,
          f'DECLARATION (VARIABLE-NO-INIT) {self.m_Args[0]!r}', fp )

        self.m_Args[1].dump( indent+1, fp = fp )

      else :
        dumpHeaderLine( indent, self.m_LineNum,
          f'DECLARATION (VARIABLE) {self.m_Args[0]!r}', fp )

        self.m_Args[1].dump( indent+1, fp = fp )
        init.dump( indent+1, fp = fp )

    elif self.m_Kind == 'FUNCTION' :
      dumpHeaderLine( indent, self.m_LineNum,
        f'DECLARATION (FUNCTION) {self.m_Args[0]!r} <{len(self.m_Args[1])}>', fp )

      for lineno, id_, type_ in self.m_Args[1] :
        dumpHeaderLine( indent+1, lineno, f'FORMAL {id_!r}', fp )
        type_.dump( indent+2, fp = fp )

      self.m_Args[2].dump( indent+1, fp = fp )
      self.m_Args[3].dump( indent+1, fp = fp )

    else :
      dumpHeaderLine( indent, self.m_LineNum,
        f'DECLARATION ({self.m_Kind!r}) unknown', fp )

  def semantic( self, symbolTable ) :
    var_name = self.m_Args[0]
    var_type = self.m_Args[1].semantic( symbolTable )

    exists = symbolTable.nameExistsInCurrentScope( var_name )

    if exists:
      raise SemanticError( f'({self.m_LineNum}) Variable name {var_name} redeclared.' )

    entry = symbolTable.addName( var_name, var_type, self.m_LineNum )

    if self.m_Args[2]:
      return ( 'VARIABLE_INIT', entry.qualifiedName, self.m_Args[2].semantic( symbolTable ) )
    else:
      return ( 'VARIABLE_INIT', entry.qualifiedName, ( 'EXPR', ( 'LITERAL', ), var_type, True, DEFAULT_VALUE[ var_type ] ) )

#---------#---------#---------#---------#---------#--------#
