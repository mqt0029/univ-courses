# Tram, Minh
# mqt0029
# 2019-04-30

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2019 Spring semester.

#----------------------------------------------------------------------
import tkinter as tk
import math
from tkinter import simpledialog
from tkinter import filedialog

import ModelData as md
import constructTransform as cf

#----------------------------------------------------------------------
class cl_widgets :
  def __init__( self, ob_root_window, ob_world = [] ) :
    self.clipenabled = tk.BooleanVar(value = False)
    self.perspective = tk.BooleanVar(value = False)
    self.eulerrotate = tk.BooleanVar(value = False)

    self.view_distance = 0
    self.res = 4

    self.m_Phi, self.m_Theta, self.m_Psi = 0.0, 0.0, 0.0

    self.ob_root_window = ob_root_window
    self.ob_world = ob_world

    self.menu = cl_menu( self )
    self.toolbar = cl_toolbar( self )

    self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
    self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.statusBar_frame.set( 'This is the status bar' )

    self.ob_canvas_frame = cl_canvas_frame( self )
    self.ob_world.add_canvas( self.ob_canvas_frame.canvas )

    self.model = None

#----------------------------------------------------------------------
class cl_canvas_frame :
  def __init__( self, master ) :
    self.master = master
    self.canvas = tk.Canvas(
      master.ob_root_window, width=1, height=1, bg='black' )

    self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
    self.canvas.bind( '<Configure>',       self.canvas_resized_callback )
    self.canvas.bind( '<Key>',             self.key_callback )

    self.canvas.bind( '<ButtonPress-1>',   lambda e : self.btn_callback( 'LMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-1>', lambda e : self.btn_callback( 'LMB', 'release', e ) )
    self.canvas.bind( '<B1-Motion>',       lambda e : self.btn_callback( 'LMB', 'motion', e ) )
    self.canvas.bind( '<ButtonPress-2>',   lambda e : self.btn_callback( 'MMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-2>', lambda e : self.btn_callback( 'MMB', 'release', e ) )
    self.canvas.bind( '<B2-Motion>',       lambda e : self.btn_callback( 'MMB', 'motion', e ) )
    self.canvas.bind( '<ButtonPress-3>',   lambda e : self.btn_callback( 'RMB', 'press', e ) )
    self.canvas.bind( '<ButtonRelease-3>', lambda e : self.btn_callback( 'RMB', 'release', e ) )
    self.canvas.bind( '<B3-Motion>',       lambda e : self.btn_callback( 'RMB', 'motion', e ) )

    self.canvas.bind( '<4>',                 lambda e : self.btn_callback( 'Mouse wheel', 'zoomout', e ) )
    self.canvas.bind( '<5>',                 lambda e : self.btn_callback( 'Mouse wheel', 'zoomin', e ) )

    self.canvas.bind( '<Up>',              lambda e : self.arrow_callback( 'Up', False, e ) )
    self.canvas.bind( '<Down>',            lambda e : self.arrow_callback( 'Down', False, e ) )
    self.canvas.bind( '<Right>',           lambda e : self.arrow_callback( 'Right', False, e ) )
    self.canvas.bind( '<Left>',            lambda e : self.arrow_callback( 'Left', False, e ) )
    self.canvas.bind( '<Shift-Up>',        lambda e : self.arrow_callback( 'Up', True, e ) )
    self.canvas.bind( '<Shift-Down>',      lambda e : self.arrow_callback( 'Down', True, e ) )
    self.canvas.bind( '<Shift-Right>',     lambda e : self.arrow_callback( 'Right', True, e ) )
    self.canvas.bind( '<Shift-Left>',      lambda e : self.arrow_callback( 'Left', True, e ) )

  def arrow_callback( self, arrow, shift, event ) :
    shiftValue = 'Shift-' if shift else ''
    self.master.statusBar_frame.set( f'{shiftValue}{arrow} arrow pressed.' )

  def btn_callback( self, btn, action, event ) :
    if action == 'press' :
      self.master.statusBar_frame.set( f'{btn} pressed. ({event.x}, {event.y})' )
      self.x = event.x
      self.y = event.y
      self.canvas.focus_set()

    elif action == 'release' :
      self.master.statusBar_frame.set( f'{btn} released. ({event.x}, {event.y})' )
      self.x = None
      self.y = None

    elif action == 'motion' :
      self.master.statusBar_frame.set( f'{btn} dragged. ({event.x}, {event.y})' )
      self.x = event.x
      self.y = event.y

    elif action == 'zoomout' :
      self.master.view_distance -= 0.1 * self.master.view_distance
      self.master.ob_world.reset()
      self.master.toolbar.draw_callback()
      self.master.statusBar_frame.set( f'{btn} scrolled. Current distance is {self.master.view_distance}.' )

    elif action == 'zoomin' :
      self.master.view_distance += 0.1 * self.master.view_distance
      self.master.ob_world.reset()
      self.master.toolbar.draw_callback()
      self.master.statusBar_frame.set( f'{btn} scrolled. Current distance is {self.master.view_distance}.' )

    # elif action == 'roll-down':
    #   self.master.m_Phi -= 1
    #   self.master.ob_world.reset()
    #   self.master.toolbar.draw_callback()
    #   self.master.statusBar_frame.set( f'Current angles φ = {self.master.m_Phi} θ = {self.master.m_Theta} ψ = {self.master.m_Psi} (degrees)' )

    # elif action == 'roll-up':
    #   self.master.m_Phi += 1
    #   self.master.ob_world.reset()
    #   self.master.toolbar.draw_callback()
    #   self.master.statusBar_frame.set( f'Current angles φ = {self.master.m_Phi} θ = {self.master.m_Theta} ψ = {self.master.m_Psi} (degrees)' )

    # elif action == 'pitch-down':
    #   self.master.m_Theta -= 1
    #   self.master.ob_world.reset()
    #   self.master.toolbar.draw_callback()
    #   self.master.statusBar_frame.set( f'Current angles φ = {self.master.m_Phi} θ = {self.master.m_Theta} ψ = {self.master.m_Psi} (degrees)' )

    # elif action == 'pitch-up':
    #   self.master.m_Theta += 1
    #   self.master.ob_world.reset()
    #   self.master.toolbar.draw_callback()
    #   self.master.statusBar_frame.set( f'Current angles φ = {self.master.m_Phi} θ = {self.master.m_Theta} ψ = {self.master.m_Psi} (degrees)' )

    # elif action == 'yaw-down':
    #   self.master.m_Psi -= 1
    #   self.master.ob_world.reset()
    #   self.master.toolbar.draw_callback()
    #   self.master.statusBar_frame.set( f'Current angles φ = {self.master.m_Phi} θ = {self.master.m_Theta} ψ = {self.master.m_Psi} (degrees)' )

    # elif action == 'yaw-up':
    #   self.master.m_Psi += 1
    #   self.master.ob_world.reset()
    #   self.master.toolbar.draw_callback()
    #   self.master.statusBar_frame.set( f'Current angles φ = {self.master.m_Phi} θ = {self.master.m_Theta} ψ = {self.master.m_Psi} (degrees)' )

    else :
      self.master.statusBar_frame.set( f'Unknown {btn} action {action}.' )

  def key_callback( self, event ) :
    msg = f'{event.char!r} ({ord( event.char )})' \
      if len( event.char ) > 0 else '<non-printing char>'

    self.master.statusBar_frame.set(
      f'{msg} pressed at ({event.x},{event.y})' )

  def canvas_resized_callback( self, event ) :
    self.canvas.config( width = event.width-4, height = event.height-4 )

    self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.master.statusBar_frame.set(
      f'Canvas width, height ({self.canvas.cget( "width" )}, ' +
      f'{self.canvas.cget( "height" )})' )

    self.canvas.pack()

#----------------------------------------------------------------------
class cl_statusBar_frame( tk.Frame ) :
  def __init__( self, master ) :
    tk.Frame.__init__( self, master )
    self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
    self.label.pack( fill = tk.X )

  def set( self, formatStr, *args ) :
    self.label.config( text = "mqt0029: " + formatStr % args )
    self.label.update_idletasks()

  def clear( self ) :
    self.label.config( text='' )
    self.label.update_idletasks()

#----------------------------------------------------------------------
class cl_menu :
  def __init__( self, master ) :
    self.master = master
    self.menu = tk.Menu( master.ob_root_window )
    master.ob_root_window.config( menu = self.menu )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'File', menu = dummy )
    dummy.add_command( label = 'New', command = lambda : self.menu_callback( 'file>new' ) )
    dummy.add_command( label = 'Open...', command = lambda : self.menu_callback( 'file>open' ) )
    dummy.add_separator()
    dummy.add_command( label = 'Exit', command = lambda : self.menu_callback( 'file>exit' ) )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Settings', menu = dummy )
    dummy.add_checkbutton( label = 'Clip', variable = self.master.clipenabled, command = lambda : self.menu_callback( 'Clipping is set to ' + str( self.master.clipenabled.get() ) ) )
    dummy.add_checkbutton( label = 'Perspective', variable = self.master.perspective, command = lambda : self.menu_callback( 'Perspective is set to ' + str( self.master.perspective.get() ) ) )
    dummy.add_checkbutton( label = 'Euler', variable = self.master.eulerrotate, command = lambda : self.menu_callback( 'Euler rotation is set to ' + str( self.master.eulerrotate.get() ) ) )

    dummy = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Help', menu = dummy )
    dummy.add_command( label = 'About...', command = lambda : self.menu_callback( 'help>about' ) )

  def menu_callback( self, which = None ) :
    item = 'menu' if which is None else which
    self.master.statusBar_frame.set( f'{item!r} callback' )

#----------------------------------------------------------------------
class cl_toolbar :
  def __init__( self, master ) :
    self.master = master
    self.toolbar = tk.Frame( master.ob_root_window )

    dummy = tk.Button( self.toolbar, text = 'Resolution', width = 8, command = self.resolution_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Distance', width = 8, command = self.distance_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'φ', width = 4, command = self.phi_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'θ', width = 4, command = self.theta_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'ψ', width = 4, command = self.psi_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Reset', width = 8, command = self.reset_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Load', width = 8, command = self.load_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    dummy = tk.Button( self.toolbar, text = 'Draw', width = 8, command = self.draw_callback )
    dummy.pack( side = tk.LEFT, padx = 2, pady = 2 )

    self.toolbar.pack( side = tk.TOP, fill = tk.X )

  def phi_callback( self ):
    n_Phi = simpledialog.askfloat( title = 'φ (phi) value change', prompt = 'Enter new value for φ (phi)', initialvalue = self.master.m_Phi )
    if n_Phi is None:
      self.master.statusBar_frame.set( f'User cancelled. φ (phi) value remains {self.master.m_Phi} degrees' )
    else:
      self.master.m_Phi = n_Phi
      self.master.statusBar_frame.set( f'φ (phi) value changed. φ (phi) is now {self.master.m_Phi} degrees' )

  def theta_callback( self ):
    n_Theta = simpledialog.askfloat( title = 'θ (theta) value change', prompt = 'Enter new value for θ (theta)', initialvalue = self.master.m_Theta )
    if n_Theta is None:
      self.master.statusBar_frame.set( f'User cancelled. θ (theta) value remains {self.master.m_Theta} degrees' )
    else:
      self.master.m_Theta = n_Theta
      self.master.statusBar_frame.set( f'θ (theta) value changed. θ (theta) is now {self.master.m_Theta} degrees' )

  def psi_callback( self ):
    n_Psi = simpledialog.askfloat( title = 'ψ (psi) value change', prompt = 'Enter new value for ψ (psi)', initialvalue = self.master.m_Psi )
    if n_Psi is None:
      self.master.statusBar_frame.set( f'User cancelled. ψ (psi) value remains {self.master.m_Psi} degrees' )
    else:
      self.master.m_Psi = n_Psi
      self.master.statusBar_frame.set( f'ψ (psi) value changed. ψ (psi) is now {self.master.m_Psi} degrees' )

  def resolution_callback( self ):
    newresolution = simpledialog.askinteger( 'Set resolution', 'Enter new integer resolution value', initialvalue = self.master.res, minvalue = 4 )
    if newresolution is not None:
      self.master.res = newresolution
      self.master.statusBar_frame.set( f'Resolution changed. Current resolution is {self.master.res}' )
    else:
      self.master.statusBar_frame.set( f'User cancelled. Current resolution remains {self.master.res} ' )

  def distance_callback( self ):
    newdistance = simpledialog.askfloat( 'Distance callback', 'Enter new distance value', initialvalue = self.master.view_distance, minvalue = 0 )
    if newdistance is not None:
      self.master.view_distance = newdistance
      self.master.statusBar_frame.set( f'View distance changed. Current distance is {self.master.view_distance} ' )
    else:
      self.master.statusBar_frame.set( f'User cancelled. Current distance remains {self.master.view_distance} ' )

  def reset_callback( self ) :
    self.master.ob_world.reset()
    self.master.statusBar_frame.set( 'Reset callback' )

  def load_callback( self ) :
    filename = tk.filedialog.askopenfilename( filetypes = [ ( "allfiles", "*" ) ] )

    if len( filename ) is 0:
      self.master.statusBar_frame.set( 'User cancelled' )
    else:
      self.master.model = md.ModelData()
      self.master.model.loadFile( filename )
      self.master.statusBar_frame.set( 'Load callback' )

  def draw_callback( self ) :
    if self.master.model is None:
      self.master.statusBar_frame.set( 'Mesh not loaded' )
    else:
      canW = int( self.master.ob_canvas_frame.canvas.cget( "width" ) )
      canH = int( self.master.ob_canvas_frame.canvas.cget( "height" ) )
      window  = self.master.model.getWindow()
      viewport = self.master.model.getViewport()
      vxmin = canW * viewport[0]
      vymin = canH * viewport[1]
      vxmax = canW * viewport[2]
      vymax = canH * viewport[3]
      self.master.model.specifyTransform( *cf.constructTransform( window, viewport, canW, canH ), self.master.view_distance )
      self.master.model.specifyEuler( self.master.m_Phi * ( math.pi / 180.0 ), self.master.m_Theta * ( math.pi / 180.0 ), self.master.m_Psi * ( math.pi / 180.0 ) )
      self.master.ob_world.create_graphic_objects( self.master.ob_canvas_frame.canvas, self.master.model, self.master.clipenabled.get(), self.master.perspective.get(), self.master.eulerrotate.get(), self.master.res )
      self.master.ob_canvas_frame.canvas.create_rectangle( vxmin, vymin, vxmax, vymax, outline='white' )
      self.master.statusBar_frame.set( 'Draw callback' )

#----------------------------------------------------------------------
