# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13

import sys
import math

class ModelData() :
  def __init__( self, inputFile = None ) :
    self.m_Vertices = []
    self.m_Faces    = []
    self.m_Window   = []
    self.m_Viewport = []
    self.m_Patches  = []

    self.m_minX     = float( '+inf' )
    self.m_maxX     = float( '-inf' )
    self.m_minY     = float( '+inf' )
    self.m_maxY     = float( '-inf' )
    self.m_minZ     = float( '+inf' )
    self.m_maxZ     = float( '-inf' )

    self.ax = 0
    self.ay = 0
    self.sx = 0
    self.sy = 0
    self.distance = 0

    self.r00 = 0.0
    self.r01 = 0.0
    self.r02 = 0.0
    self.r10 = 0.0
    self.r11 = 0.0
    self.r12 = 0.0
    self.r20 = 0.0
    self.r21 = 0.0
    self.r22 = 0.0

    self.ex = 0.0
    self.ey = 0.0
    self.ez = 0.0

    self.have_w = False
    self.have_s = False

    if inputFile is not None :
      # File name was given.  Read the data from the file.
      self.loadFile( inputFile )

  def loadFile( self, inputFile ) :
    with open( inputFile, 'r' ) as fp :
      lines = fp.read().replace('\r', '' ).split( '\n' )

    for ( index, line ) in enumerate( lines, start = 1 ) :
      line = line.strip()
      if ( line == '' or line[ 0 ] == '#' ) :
        continue

      if ( line[ 0 ] == 'v' ) :
        try :
          ( _, x, y, z ) = line.split()
          x = float( x )
          y = float( y )
          z = float( z )

          self.m_minX = min( self.m_minX, x )
          self.m_maxX = max( self.m_maxX, x )
          self.m_minY = min( self.m_minY, y )
          self.m_maxY = max( self.m_maxY, y )
          self.m_minZ = min( self.m_minZ, z )
          self.m_maxZ = max( self.m_maxZ, z )

          self.m_Vertices.append( ( x, y, z ) )

        except :
          print( 'Line %d is a malformed vertex spec.' % index )

      elif ( line[ 0 ] == 'f' ) :
        try :
          ( _, v1, v2, v3 ) = line.split()
          v1 = int( v1 )-1
          v2 = int( v2 )-1
          v3 = int( v3 )-1
          self.m_Faces.append( ( v1, v2, v3 ) )

        except :
          print( 'Line %d is a malformed face spec.' % index )

      elif ( line[ 0 ] == 'w' ) :
        try :
          ( _, w1, w2, w3, w4 ) = line.split()
          w1 = float( w1 )
          w2 = float( w2 )
          w3 = float( w3 )
          w4 = float( w4 )

          if self.have_w is False:
            self.m_Window = ( w1, w2, w3, w4 )
            self.have_w = True
          else:
            self.m_Window = ( w1, w2, w3, w4 )
            print( 'Line %d is a duplicate window spec.' % index )
        
        except :
          print( 'Line %d is a malformed window spec.' % index )

      elif ( line[ 0 ] == 's' ):
        try :
          ( _, s1, s2, s3, s4 ) = line.split()
          s1 = float( s1 )
          s2 = float( s2 )
          s3 = float( s3 )
          s4 = float( s4 )

          if self.have_s is False:
            self.m_Viewport = ( s1, s2, s3, s4 )
            self.have_s = True
          else:
            self.m_Viewport = ( s1, s2, s3, s4 )
            print( 'Line %d is a duplicate viewport spec.' % index )

        except :
          print( 'Line %d is a malformed viewport spec.' % index )

      elif ( line[ 0 ] == 'p' and len( line.split() ) == 17 ):
        try :
          self.m_Patches.append( tuple( [ int( x ) - 1 for x in line.split()[ 1: ] ] ) )
        
        except :
          print( 'Line %d is a malformed patch spec.' % index ) 

      else :
          print( 'Line %d \'%s\' is unrecognized.' % ( index, line ) )

  def getCenter( self ) :
    return (
      ( self.m_minX + self.m_maxX ) / 2.0,
      ( self.m_minY + self.m_maxY ) / 2.0,
      ( self.m_minZ + self.m_maxZ ) / 2.0 )

  def specifyEuler( self, phi, theta, psi ):
    self.r00   = math.cos( psi ) * math.cos( theta )
    self.r01   = -1 * math.cos( theta ) * math.sin( psi )
    self.r02   = math.sin( theta )
    self.r10  = math.cos( phi ) * math.sin( psi ) + math.cos( psi ) * math.sin( phi ) * math.sin( theta )
    self.r11  = math.cos( phi ) * math.cos( psi ) - math.sin( phi ) * math.sin( psi ) * math.sin( theta )
    self.r12  = -1 * math.cos( theta ) * math.sin( phi )
    self.r20  = -1 * math.cos( phi ) * math.cos( psi ) * math.sin( theta ) + math.sin( phi ) * math.sin( psi )
    self.r21  = math.cos( phi ) * math.sin( psi ) * math.sin( theta ) + math.cos( psi ) * math.sin( phi )
    self.r22  = math.cos( phi ) * math.cos( theta )
    ( cx, cy, cz ) = self.getCenter()
    self.ex   = -1 * self.r00 * cx - self.r01 * cy - self.r02 * cz + cx
    self.ey   = -1 * self.r10 * cx - self.r11 * cy - self.r12 * cz + cy
    self.ez   = -1 * self.r20 * cx - self.r21 * cy - self.r22 * cz + cz

  def specifyTransform( self, ax, ay, sx, sy, d ):
    self.ax = ax
    self.ay = ay
    self.sx = sx
    self.sy = sy
    self.distance = d

  def getTransformedVertex( self, vNum, doPerspective, doEuler ):
    if doEuler:
      x = self.r00 * self.m_Vertices[vNum][0] + self.r01 * self.m_Vertices[vNum][1] + self.r02 * self.m_Vertices[vNum][2] + self.ex
      y = self.r10 * self.m_Vertices[vNum][0] + self.r11 * self.m_Vertices[vNum][1] + self.r12 * self.m_Vertices[vNum][2] + self.ey
      z = self.r20 * self.m_Vertices[vNum][0] + self.r21 * self.m_Vertices[vNum][1] + self.r22 * self.m_Vertices[vNum][2] + self.ez
    else: ( x, y, z ) = self.m_Vertices[vNum]

    if doPerspective:
      if self.distance is 0 or self.distance <= z:
        return ( ( self.getCenter()[0] ) * self.sx + self.ax, ( self.getCenter()[1] ) * self.sy + self.ay, 0 )
      else:
        perx = ( x / ( 1 - ( z / self.distance ) ) ) * self.sx + self.ax
        pery = ( y / ( 1 - ( z / self.distance ) ) ) * self.sy + self.ay
        return ( perx, pery, 0 )
    else:
      return ( x * self.sx + self.ax, y * self.sy + self.ay, 0 )

  def getFaces( self )    : return self.m_Faces
  def getVertices( self ) : return self.m_Vertices
  def getViewport( self ) : return self.m_Viewport
  def getWindow( self )   : return self.m_Window
  def getPatches( self )  : return self.m_Patches

#---------#---------#---------#---------#---------#--------#
def _main() :
  # Get the file name to load.
  fName = sys.argv[1]

  # Create a ModelData object to hold the model data from
  # the supplied file name.
  model = ModelData( fName )

  # Now that it's loaded, print out a few statistics about
  # the model data that we just loaded.
  print( f'{fName}: {len( model.getVertices() )} vert%s, {len( model.getFaces() )} face%s' % (
    'ex' if len( model.getVertices() ) == 1 else 'ices',
    '' if len( model.getFaces() ) == 1 else 's' ))

  print( 'First 3 vertices:' )
  for v in model.getVertices()[0:3] :
    print( f'     {v}' )

  print( 'First 3 faces:' )
  for f in model.getFaces()[0:3] :
    print( f'     {f}' )

  print( f'Window line    : {model.getWindow()}' )
  print( f'Viewport line  : {model.getViewport()}' )

  print( f'Center         : {model.getCenter()}' )

#---------#
if __name__ == '__main__' :
  _main()

#---------#---------#---------#---------#---------#--------#
