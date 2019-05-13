# Tram, Minh
# mqt0029
# 2019-04-18

#---------#---------#---------#---------#---------#--------#
def constructTransform( w, v, width, height ) :
  wxmin, wymin, wxmax, wymax = w
  vxmin, vymin, vxmax, vymax = v

  fx, fy = -wxmin, -wymin
  gx, gy = width * vxmin, height * vymin

  sx = ( width * ( vxmax - vxmin ) ) / ( wxmax - wxmin )
  sy = ( height * ( vymax - vymin ) ) / ( wymax - wymin )

  ax = fx * sx + gx
  ay = fy * sy + gy

  return ( ax, ay, sx, sy )

#---------#---------#---------#---------#---------#--------#
def _main() :
  w      = ( -1.0, -2.0, 4.0, 5.0 )
  v      = ( 0.15, 0.15, 0.85, 0.85 )
  width  = 500
  height = 400

  values = constructTransform( w, v, width, height )
  ax, ay, sx, sy = values

  print( f'Values          : {values}' )
  print( f'Test transform  : ax {ax}, ay {ay}, sx {sx}, sy {sy}' )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
