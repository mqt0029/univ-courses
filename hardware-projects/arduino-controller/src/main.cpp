// Tram, Minh
// 2019-05-13

#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <JoystickLib.h>

#define JOYSTICK_SW 2
#define JOYSTICK_X  A2
#define JOYSTICK_Y  A3

#define XSPEED      1
#define YSPEED      2
#define ROLL        3
#define PITCH       4
#define YAW         5
#define TRIGGER     6

                    // addr,en,rw,rs,d4,d5,d6,d7,bl,blpol
LiquidCrystal_I2C lcd( 0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE );
Joystick controller( JOYSTICK_X, JOYSTICK_Y );

int dummy = 0;
int xspeed = 0, yspeed = 0;
int roll = 0;
int pitch = 0;
int yaw = 0;

void updateMeasurements( int what, int value )
{
  if ( what == ROLL || what == PITCH || what == YAW )
  {
    while ( value >= 360 || value < 0 )
    {
      if ( value >= 360 ) value -= 360;
      else if ( value < 0 ) value += 360;
    }
  }
  else if ( what == TRIGGER )
  {
    while ( value >= 99 || value < 0 )
    {
      if ( value >= 99 ) value -= 99;
      else if ( value < 0 ) value = 0;
    }
  }

  if ( what == XSPEED )
  {
    lcd.setCursor( 6, 1 );
    lcd.print( "   " );
    lcd.setCursor( 6, 1 );
  }
  else if ( what == YSPEED )
  {
    lcd.setCursor( 17, 1 );
    lcd.print( "   " );
    lcd.setCursor( 17, 1 );
  }
  else if ( what == ROLL )
  {
    lcd.setCursor( 6, 2 );
    lcd.print( "   " );
    lcd.setCursor( 6, 2 );
  }
  else if ( what == PITCH )
  {
    lcd.setCursor( 17, 2 );
    lcd.print( "   " );
    lcd.setCursor( 17, 2 );
  }
  else if ( what == YAW )
  {
    lcd.setCursor( 6, 3 );
    lcd.print( "   " );
    lcd.setCursor( 6, 3 );
  }
  else if ( what == TRIGGER )
  {
    lcd.setCursor( 17, 3 );
    lcd.print( "   " );
    lcd.setCursor( 17, 3 );
  }

  lcd.print( String( value ) );
}

void updateDirection( String direction )
{
  lcd.setCursor( 11, 0 );
  lcd.print( "         " );
  lcd.setCursor( 11, 0 );
  lcd.print( direction );
}

void readController()
{
  controller.loop();

  xspeed = controller.getX();
  yspeed = controller.getY();
  
  updateMeasurements( XSPEED, xspeed );
  updateMeasurements( YSPEED, yspeed );
  
  if ( ( xspeed > -3 && xspeed < 3 ) && ( yspeed > -3 && yspeed < 3 ) )
  {
    updateDirection( "STOP" );
  }
  else if ( controller.isUp() )
  {
    updateDirection( "FORWARD" );
  }
  else if ( controller.isRightUp() )
  {
    updateDirection( "FWD-RIGHT" );
  }
  else if ( controller.isRight() )
  {
    updateDirection( "RIGHT" );
  }
  else if ( controller.isRightDown() )
  {
    updateDirection( "REV-RIGHT" );
  }
  else if ( controller.isDown() )
  {
    updateDirection( "REVERSE" );
  }
  else if ( controller.isLeftDown() )
  {
    updateDirection( "REV-LEFT" );
  }
  else if ( controller.isLeft() )
  {
    updateDirection( "LEFT" );
  }
  else if ( controller.isLeftUp() )
  {
    updateDirection( "FWD-LEFT" );
  }
}

void setup() 
{
  // init LCD
  lcd.begin( 20, 4 );
  lcd.setCursor( 0, 0 );
  lcd.print( "Direction: " );
  lcd.setCursor( 0, 1 );
  lcd.print( "Xspd: " );
  lcd.setCursor( 10, 1 );
  lcd.print( "Yspd : " );
  lcd.setCursor( 0, 2 );
  lcd.print( "Roll:    " );
  lcd.setCursor( 10, 2 );
  lcd.print( "Pitch: " );
  lcd.setCursor( 0, 3 );
  lcd.print( "Yaw :    " );
  lcd.setCursor( 10, 3 );
  lcd.print( "Trig : " );

  updateDirection( "STOP" );
  updateMeasurements( XSPEED, 0 );
  updateMeasurements( YSPEED, 0 );
  updateMeasurements( ROLL, 0 );
  updateMeasurements( PITCH, 0 );
  updateMeasurements( YAW, 0 );
  updateMeasurements( TRIGGER, 0 );

  // Init joystick
  controller.calibrate();

  // Serial for debugging
  Serial.begin( 9600 );
}

void loop() 
{
  readController();

  
  delay( 50 );
}