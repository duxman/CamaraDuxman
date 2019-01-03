import os
import time
from config import config
from util.logger import clienteLog
from PIL import Image
from images2gif import writeGif
if os.name == 'poxis':
    import RPi.GPIO as GPIO
    import pygame
else:
    from emulators import pygame
    import tool.EmulatorGUI as GPIODEV
    GPIO = GPIODEV.emulatorGPIO()


#Constantes GPIO
BOTON_GPIO=7
LUZ_BOTON_GPIO=8
LED_VERDE_GPIO=9
LED_NARANJA_GPIO=10
LED_ROJO_GPIO=11
FLASH_GPIO=22

class CameraDuxmanV2(object):
    Loggger = None
    Configuration = None

    def __init__(self):
        cliente = clienteLog()
        self.Logger = cliente.InicializaLogConsole()
        self.Configuration = config()
        self.MainProcess()

    ## Defino funciones

    def EncenderLed(self, Port, Timeout):
        GPIO.output(Port, True)  ## Enciendo led
        if Timeout > 0:
            time.sleep(Timeout)  ## Espero el tiempo indicado

    ## Fin EncenderLed

    def ApagarLed(self, Port):
        GPIO.output(Port, False)  ## Apago el led

    ## Fin ApagarLed

    ## Funcion EncenderYApagarLed
    ##   Enciende un led y espera un tiempo determinado
    ##   Si es 0 no espera
    def EncenderYApagarLed(self, Port, Timeout):
        self.EncenderLed(Port, Timeout)
        self.ApagarLed(Port)

    ##Fin EncenderYApagarLed

    def borrar(self):
        self.Configuration.Pantalla.screen.fill((0, 0, 0))

    def damePosicionCentro(self,tam):
        Ancho = tam[0]
        Alto = tam[1]
        CentroHor = 400 - (Ancho / 2)
        CentroVer = 240 - (Alto / 2)
        return (CentroHor, CentroVer);

    def Texto(self,texto, tam):
        self.borrar()
        font = pygame.font.Font("Fine.ttf", tam)
        text_surface = font.render(texto, True, (255, 255, 255))
        textSize = font.size(texto)
        posicion = self.damePosicionCentro(textSize)

        self.Configuration.Pantalla.screen.blit(text_surface, posicion)
        pygame.display.update()

    def Setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(BOTON_GPIO, GPIO.IN)
        GPIO.setup(LUZ_BOTON_GPIO, GPIO.OUT)
        GPIO.setup(LED_VERDE_GPIO, GPIO.OUT)
        GPIO.setup(LED_NARANJA_GPIO, GPIO.OUT)
        GPIO.setup(LED_ROJO_GPIO, GPIO.OUT)
        GPIO.setup(FLASH_GPIO, GPIO.OUT)

    ## Fin PrepararGPIO

    ##NombreFichero
    def dameNombreFicheroCapturaBase(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../IMAGENES/JPG/IMG_%s" % (timestr)
        return filename

    def dameNombreFicheroGif(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../IMAGENES/GIFS/IMG_%s.gif" % (timestr)
        return filename

    ##FinNombreFichero


    def MainProcess(self):
        try:
            self.Setup()
            self.Texto("FOTOMATON DUX", 90)
            time.sleep(3)
            self.Texto("Pulsa el Boton", 90)
            while True:
                if (GPIO.input(BOTON_GPIO)):
                    ImagesToGIF = []
                    NombreBaseCaptura = self.dameNombreFicheroCapturaBase()
                    NombreGIF = self.dameNombreFicheroGif()

                    # camera.start_preview()
                    self.ApagarLed(LUZ_BOTON_GPIO)  ## Apago el la luz del boton
                    print("Button Pressed")
                    self.EncenderLed(FLASH_GPIO, 0)  ## Enciendo el Flash

                    self.Texto('3', 250)
                    self.EncenderYApagarLed(LED_ROJO_GPIO, 3)  ## Enciendo el led Rojo
                    self.Configuration.Camera.capture(NombreBaseCaptura + '_01.jpg')

                    self.Texto('2', 250)
                    self.EncenderYApagarLed(LED_NARANJA_GPIO, 3)  ## Enciendo el led Naranja
                    self.Configuration.Camera.capture(NombreBaseCaptura + '_02.jpg')

                    self.Texto('1', 250)
                    self.EncenderYApagarLed(LED_VERDE_GPIO, 3)  ## Enciendo el led Verde
                    self.Configuration.Camera.capture(NombreBaseCaptura + '_03.jpg')

                    self.Texto("SONRIE ;)", 100)
                    self.EncenderYApagarLed(LED_VERDE_GPIO, 3)  ## Enciendo el led Verde
                    self.Configuration.Camera.capture(NombreBaseCaptura + '_04.jpg')
                    self.ApagarLed(FLASH_GPIO)

                    self.Texto("Guardando ...", 100)

                    ImagesToGIF.append(Image.open(NombreBaseCaptura + '_01.jpg'))
                    ImagesToGIF.append(Image.open(NombreBaseCaptura + '_02.jpg'))
                    ImagesToGIF.append(Image.open(NombreBaseCaptura + '_03.jpg'))
                    ImagesToGIF.append(Image.open(NombreBaseCaptura + '_04.jpg'))

                    writeGif(NombreGIF, ImagesToGIF, duration=0.5)

                    # camera.stop_preview()
                    self.Texto("Pulsa el Boton", 90)
                else:
                    self.EncenderLed(LUZ_BOTON_GPIO, 0)  ## Enciendo el LUZ_BOTON_GPIO
                    self.ApagarLed(LED_ROJO_GPIO)  ## Apago el led Rojo
                    self.ApagarLed(LED_NARANJA_GPIO)  ## Apago el led Naranja
                    self.ApagarLed(LED_VERDE_GPIO)  ## Apago el led Verde
                    ##Fin if Boton
                    ##Fin While
        except Exception as ex:
            self.Logger.critical( str(ex) )
        finally:
            self.Logger.info( "Ejecucion finalizada" )
            GPIO.cleanup()


if __name__ == "__main__":
    mainprogram = CameraDuxmanV2()
    mainprogram.MainProcess()

    mainprogram.Logger.info("--------------------<<  END  >>--------------------")
