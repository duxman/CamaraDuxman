import os
import threading
import time
import Queue
import cv2
import pygame

from PIL import Image

from util.HiloCaptura import WriterCaptura
from util.config import configuration
from util.images2gif import writeGif
from util.logger import clienteLog

# solo para emular el GPIO
if os.name == 'poxis':
    import RPi.GPIO as GPIO
else:
    from emulators import emuladores_debug
    GPIO = emuladores_debug.emulatorGPIO()


#Constantes GPIO
class CameraDuxmanV2(object):
    Loggger = None
    Configuration = None
    ret = None
    CurrentFrame = None
    ColaDatos = None
    hiloCaptura = None


    def __init__(self):
        cliente = clienteLog()


        self.Logger = cliente.InicializaLogConsole()
        self.Configuration = configuration(self.Logger)
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
        font = pygame.font.Font("./resources/Fine.ttf", tam)
        text_surface = font.render(texto, True, (255, 255, 255))
        textSize = font.size(texto)
        posicion = self.damePosicionCentro(textSize)

        self.Configuration.Pantalla.screen.blit(text_surface, posicion)
        pygame.display.update()

    def Setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.Configuration.BOTON_GPIO, GPIO.IN)
        GPIO.setup(self.Configuration.LUZ_BOTON_GPIO, GPIO.OUT)
        GPIO.setup(self.Configuration.LED_VERDE_GPIO, GPIO.OUT)
        GPIO.setup(self.Configuration.LED_NARANJA_GPIO, GPIO.OUT)
        GPIO.setup(self.Configuration.LED_ROJO_GPIO, GPIO.OUT)
        GPIO.setup(self.Configuration.FLASH_GPIO, GPIO.OUT)

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

    def tomarFoto(self,texto,tamtexto,led_aviso,timeout,nombrebasecaptura, numeroimagen):

        nombrefotofinal = nombrebasecaptura + '_' + format(numeroimagen, '02d') + '.jpg'

        self.Logger.info("capturamos una foto" + nombrefotofinal)

        self.Texto(texto, tamtexto) # Muestro el texto por pantalla
        self.EncenderYApagarLed(led_aviso, timeout)  ## Enciendo el led
        #self.Configuration.Camera.capture(nombrefotofinal) # capturo la imagen
        self.captureImagen(nombrefotofinal)

    def generateGIF(self, numimages, nombrebasecaptura, nombregif,duracion):
        self.Logger.info("Creamos hilo gif ")
        # Esto le cuesta bastante lo ejecutamos en un hilo en 2 plano ya acabara
        producer = threading.Thread(target=self.createGIF(numimages, nombrebasecaptura, nombregif,duracion), name="GIFManagerThread")
        # Indicamos que es un daemon
        producer.daemon = True
        #iniciamos el hilo
        producer.start()

    def createGIF(self, numimages, nombrebasecaptura, nombregif,duracion):
        imgforgif = []
        self.Logger.info("Creamos gif " + nombregif )
        # Cargamos las imagenes en el vector
        for i in range(numimages):
            imgforgif.append(Image.open(nombrebasecaptura +  format(i + 1, '02d') + '.jpg'))

        # escribimos el gif en el disco
        writeGif(nombregif, imgforgif, duration=duracion)

    def captureImagen(self,nombrefotofinal):
        if( self.Configuration.TipoCamara == "RPI" ):
            self.Configuration.Camera.capture(nombrefotofinal)  # capturo la imagen por raspberry
        else:
             self.Configuration.Camera.imwrite(nombrefotofinal,self.ColaDatos.get(True,1) )

    def hiloCapturaWindows(self):
        self.ColaDatos = Queue.LifoQueue()
        self.hiloCaptura = WriterCaptura(self.ColaDatos, self.Configuration.Camera)
        self.hiloCaptura.start()


    def MainProcess(self):
        try:
            self.Setup()
            self.Texto("FOTOMATON DUX", 90)
            time.sleep(3)
            self.Texto("Pulsa el Boton", 90)
            while True:
                if (GPIO.input(self.Configuration.BOTON_GPIO)):

                    NombreBaseCaptura = self.dameNombreFicheroCapturaBase()
                    NombreGIF = self.dameNombreFicheroGif()

                    self.Texto("Preparando...", 100)
                    self.hiloCapturaWindows()
                    time.sleep(1)

                    self.Texto("Todo listo", 100)

                    self.Logger.info("Encendemos el flash")
                    # camera.start_preview()
                    self.ApagarLed(self.Configuration.LUZ_BOTON_GPIO)  ## Apago el la luz del boton
                    self.Logger.info("Button Pressed")


                    self.EncenderLed(self.Configuration.FLASH_GPIO, 0)  ## Enciendo el Flash

                    self.tomarFoto('3',250,self.Configuration.LED_ROJO_GPIO,3,NombreBaseCaptura,1)
                    self.tomarFoto('2',250, self.Configuration.LED_NARANJA_GPIO, 3, NombreBaseCaptura, 2)
                    self.tomarFoto('1',250, self.Configuration.LED_VERDE_GPIO, 3, NombreBaseCaptura, 3)
                    self.tomarFoto('SONRIE :)',100, self.Configuration.LED_VERDE_GPIO, 3, NombreBaseCaptura, 4)

                    self.hiloCaptura.Stop = True

                    self.ApagarLed(self.Configuration.FLASH_GPIO)
                    self.Logger.info("flash apagado")

                    self.Texto("Guardando ...", 100)
                    self.Logger.info("Guardando las fototos")


                    self.generateGIF(NombreBaseCaptura,4,NombreGIF, 0.5)

                    # camera.stop_preview()
                    self.Texto("Pulsa el Boton", 90)
                    self.Logger.info("Volvemos a empezar")
                else:
                    self.EncenderLed(self.Configuration.LUZ_BOTON_GPIO, 0)  ## Enciendo el LUZ_BOTON_GPIO
                    self.ApagarLed(self.Configuration.LED_ROJO_GPIO)  ## Apago el led Rojo
                    self.ApagarLed(self.Configuration.LED_NARANJA_GPIO)  ## Apago el led Naranja
                    self.ApagarLed(self.Configuration.LED_VERDE_GPIO)  ## Apago el led Verde
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
