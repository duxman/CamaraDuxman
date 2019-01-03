from picamera import PiCamera
from images2gif import writeGif
from PIL import Image
import os
import time
import traceback
import RPi.GPIO as GPIO
import pygame
from CameraExtraGrafica import *

#Constantes GPIO
BOTON_GPIO=7
LUZ_BOTON_GPIO=8
LED_VERDE_GPIO=9
LED_NARANJA_GPIO=10
LED_ROJO_GPIO=11
FLASH_GPIO=22

#Defino variables generales


## Defino funciones 

def EncenderLed( Port, Timeout ):
  GPIO.output( Port, True )	## Enciendo led
  if Timeout > 0:
    time.sleep( Timeout )	## Espero el tiempo indicado  
## Fin EncenderLed

def ApagarLed( Port ):
  GPIO.output( Port, False )	## Apago el led
## Fin ApagarLed

## Funcion EncenderYApagarLed 
##   Enciende un led y espera un tiempo determinado
##   Si es 0 no espera
def EncenderYApagarLed( Port, Timeout ):
  EncenderLed( Port, Timeout )
  ApagarLed( Port )
##Fin EncenderYApagarLed

def borrar():
  pantalla.screen.fill((0,0,0))

def damePosicionCentro( tam ):
  Ancho	= tam[0]
  Alto	= tam[1]
  CentroHor = 400 - ( Ancho / 2 )
  CentroVer = 240 - ( Alto  / 2 )
  return ( CentroHor, CentroVer );



def Texto( texto, tam ):
  borrar()
  font = pygame.font.Font("Fine.ttf",tam )
  text_surface = font.render( texto, True, (255,255,255))
  textSize = font.size( texto )
  posicion = damePosicionCentro ( textSize )
  print textSize
  print posicion

  pantalla.screen.blit(text_surface, posicion )
  pygame.display.update()

def Setup():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  GPIO.setup( BOTON_GPIO,  GPIO.IN)
  GPIO.setup( LUZ_BOTON_GPIO, GPIO.OUT)
  GPIO.setup( LED_VERDE_GPIO, GPIO.OUT)
  GPIO.setup( LED_NARANJA_GPIO, GPIO.OUT)
  GPIO.setup( LED_ROJO_GPIO, GPIO.OUT)
  GPIO.setup( FLASH_GPIO, GPIO.OUT)
## Fin PrepararGPIO

##CreaDirectorios
def creadirectorios():
  rutaimagenes = '../IMAGENES' 
  rutagifs = '../IMAGENES/GIFS' 
  rutacapturas = '../IMAGENES/JPG' 
  if not os.path.exists(rutaimagenes): os.makedirs(rutaimagenes)
  if not os.path.exists(rutagifs): os.makedirs(rutagifs)
  if not os.path.exists(rutacapturas): os.makedirs(rutacapturas)
##FIN CreaDirectorios

##NombreFichero
def dameNombreFicheroCapturaBase():
  timestr = time.strftime("%Y%m%d-%H%M%S")
  filename = "../IMAGENES/JPG/IMG_%s" % (timestr)
  return filename
def dameNombreFicheroGif():
  timestr = time.strftime("%Y%m%d-%H%M%S")
  filename = "../IMAGENES/GIFS/IMG_%s.gif" % (timestr)
  return filename
##FinNombreFichero


##Funcion Main Principal
def Main():
  try:
    Setup()
    Texto( "FOTOMATON DUX", 90)
    time.sleep( 3 )
    Texto( "Pulsa el Boton", 90 )                
    while True:
      if (GPIO.input(BOTON_GPIO)):
        ImagesToGIF=[]
        NombreBaseCaptura = dameNombreFicheroCapturaBase()
        NombreGIF 	  = dameNombreFicheroGif()

        #camera.start_preview()
        ApagarLed( LUZ_BOTON_GPIO)			## Apago el la luz del boton
        print("Button Pressed")
        EncenderLed( FLASH_GPIO, 0 )		## Enciendo el Flash        
 
        Texto( '3', 250 )
        EncenderYApagarLed( LED_ROJO_GPIO, 3 )		## Enciendo el led Rojo
        camera.capture(NombreBaseCaptura+'_01.jpg')
        
        Texto( '2', 250 )
        EncenderYApagarLed( LED_NARANJA_GPIO, 3 )	## Enciendo el led Naranja
        camera.capture(NombreBaseCaptura+'_02.jpg')
        
        Texto( '1', 250 )
        EncenderYApagarLed( LED_VERDE_GPIO, 3 )		## Enciendo el led Verde
        camera.capture(NombreBaseCaptura+'_03.jpg')
        
        Texto( "SONRIE ;)", 100 )                
        EncenderYApagarLed( LED_VERDE_GPIO, 3 )		## Enciendo el led Verde
        camera.capture(NombreBaseCaptura+'_04.jpg')
	ApagarLed( FLASH_GPIO )
        
        Texto( "Guardando ...", 100 )
                
        ImagesToGIF.append(Image.open(NombreBaseCaptura+'_01.jpg'))
        ImagesToGIF.append(Image.open(NombreBaseCaptura+'_02.jpg'))
        ImagesToGIF.append(Image.open(NombreBaseCaptura+'_03.jpg'))
        ImagesToGIF.append(Image.open(NombreBaseCaptura+'_04.jpg'))
	
	writeGif(NombreGIF, ImagesToGIF,duration=0.5)


	#camera.stop_preview()
        Texto( "Pulsa el Boton", 90 )                
      else:
        EncenderLed( LUZ_BOTON_GPIO, 0)		## Enciendo el LUZ_BOTON_GPIO
        ApagarLed( LED_ROJO_GPIO )		## Apago el led Rojo
        ApagarLed( LED_NARANJA_GPIO )		## Apago el led Naranja
        ApagarLed( LED_VERDE_GPIO )		## Apago el led Verde                
      ##Fin if Boton
    ##Fin While
  except Exception as ex:
    traceback.print_exc()
  finally:
    print "Ejecucion finalizada"
    GPIO.cleanup()
  #Fin Try
##Fin Funcion Main

######################################################################################
##                           INICIO PROGRAMA
######################################################################################

pantalla = pyscope();
camera = PiCamera(resolution=(640, 480), framerate=15)
camera.iso = 600
time.sleep(2)
camera.shutter_speed = camera.exposure_speed
camera.shutter_speed = 100000
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

creadirectorios()
Main()

######################################################################################
##                           FIN PROGRAMA
######################################################################################



  




