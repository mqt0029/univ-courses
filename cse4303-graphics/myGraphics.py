# Tram, Minh
# mqt0029
# 1001540029
# 2019-05-13

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2019 Spring semester.

#----------------------------------------------------------------------
import ModelData as md
import constructTransform as cf
import numpy as np
import pprint as pp
import math
from CohenSutherland import clipLine

class cl_world :
  def __init__( self, objects = [], canvases = [] ) :
    self.canvases = canvases

  def add_canvas( self, canvas ) :
    self.canvases.append( canvas )
    canvas.world = self

  def reset( self ) :
    for canvas in self.canvases :
      canvas.delete( 'all' )

  def get_coeff( self, u, v ):
    coeff = []
    up = -u + 1
    vp = -v + 1

    coeff.append( math.pow( up, 3 ) * math.pow( vp, 3 ) )
    coeff.append( 3 * v * math.pow( up, 3 ) * math.pow( vp, 2 ) )
    coeff.append( 3 * math.pow( v, 2 ) * math.pow( up, 3 ) * vp )
    coeff.append( math.pow( v, 3 ) * math.pow( up, 3 ) )

    coeff.append( 3 * u * math.pow( up, 2 ) * math.pow( vp, 3 ) )
    coeff.append( 9 * u * v * math.pow( up, 2 ) * math.pow( vp, 2 ) )
    coeff.append( 9 * u * math.pow( v, 2 ) * math.pow( up, 2 ) * vp )
    coeff.append( 3 * u * math.pow( v, 3 ) * math.pow( up, 2 ) )

    coeff.append( 3 * math.pow( u, 2 ) * up * math.pow( vp, 3 ) )
    coeff.append( 9 * math.pow( u, 2 ) * v * up * math.pow( vp, 2 ) )
    coeff.append( 9 * math.pow( u, 2 ) * math.pow( v, 2 ) * up * vp )
    coeff.append( 3 * math.pow( u, 2 ) * math.pow( v, 3 ) * up )

    coeff.append( math.pow( u, 3 ) * math.pow( vp, 3 ) )
    coeff.append( 3 * math.pow( u, 3 ) * v * math.pow( vp, 2 ) )
    coeff.append( 3 * math.pow( u, 3 ) * math.pow( v, 2 ) * vp )
    coeff.append( math.pow( u, 3 ) * math.pow( v, 3 ) )

    return coeff

  def compute_point( self, u, v, pts ):
    c = self.get_coeff( u, v )
    point = [ 0.0, 0.0 ]
    for i in range( 0, len( c ) ) :
      point[0] = point[0] + c[i] * pts[i][0]
      point[1] = point[1] + c[i] * pts[i][1]
    return point

  def resolveBezierPatch( self, res, pts ):
    points = []
    for u in np.linspace( 0.0, 1.0, res ):
      for v in np.linspace( 0.0, 1.0, res ):
        points.append( self.compute_point( u, v, pts ) )
    return points

  def draw_triangle( self, canvas, v1, v2, v3, portal, doClip ):
    if doClip:
      l1 = clipLine( *v1, *v2, portal )
      l2 = clipLine( *v2, *v3, portal )
      l3 = clipLine( *v3, *v1, portal )
      if l1[0] is True: canvas.create_line( *l1[1:], fill = 'white' )
      if l2[0] is True: canvas.create_line( *l2[1:], fill = 'white' )
      if l3[0] is True: canvas.create_line( *l3[1:], fill = 'white' )
    else:
      canvas.create_line( *v1, *v2, *v3, *v1, fill = 'white' )

  def create_graphic_objects( self, canvas, model: md.ModelData, clipping, perspective, euler, resolution ) :
    viewport = model.getViewport()
    portal = (
      int( canvas.cget( 'width' ) )  * viewport[0],
      int( canvas.cget( 'height' ) ) * viewport[1],
      int( canvas.cget( 'width' ) )  * viewport[2],
      int( canvas.cget( 'height' ) ) * viewport[3] )
    
    for face in model.getFaces():
      v1 = model.getTransformedVertex( face[ 0 ], perspective, euler )[ :2 ]
      v2 = model.getTransformedVertex( face[ 1 ], perspective, euler )[ :2 ]
      v3 = model.getTransformedVertex( face[ 2 ], perspective, euler )[ :2 ]
      self.draw_triangle( canvas, v1, v2, v3, portal, clipping )

    for patch in model.getPatches():
      ctrlPts = [ model.getTransformedVertex( vNum, perspective, euler ) for vNum in patch ]
      pointList = self.resolveBezierPatch( resolution, ctrlPts )

      for row in range( 0, resolution - 1 ):
        rowStart = row * resolution
        for col in range( 0, resolution - 1 ):
          here = rowStart + col
          there = here + resolution
          self.draw_triangle( canvas, pointList[ here ], pointList[ there ], pointList[ there + 1 ], portal, clipping )
          self.draw_triangle( canvas, pointList[ there + 1 ], pointList[ here + 1 ], pointList[ here ], portal, clipping )

#----------------------------------------------------------------------
