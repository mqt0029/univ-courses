# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13
#---------#---------#---------#---------#---------#--------#
INDENT_STR = '  '

#---------#---------#---------#---------#---------#--------#
def dumpHeaderLine( indent, lineNum, contents, fp ) :
  print( f'({lineNum:4d}) '+(INDENT_STR*indent)+contents, file = fp )

#---------#---------#---------#---------#---------#--------#
