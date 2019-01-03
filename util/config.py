import json
import os
import time
from CameraExtraGrafica import pyscope

# Solo para emular la camara en windows
if os.name == 'poxis':
    import picamera.PiCamera as PiCamera
else:
    from emulators.emulators import PiCamera


class configuration(object):

    Pantalla = None
    Camera = None
    RutaImagenes = '../IMAGENES'
    RutaGifs = '../IMAGENES/GIFS'
    RutaCapturas = '../IMAGENES/JPG'

    BOTON_GPIO = 7
    LUZ_BOTON_GPIO = 8
    LED_VERDE_GPIO = 9
    LED_NARANJA_GPIO = 10
    LED_ROJO_GPIO = 11
    FLASH_GPIO = 22

    def __init__(self):
        self.LoadJson()
        self.Pantalla = pyscope();
        self.Camera = PiCamera(resolution=(640, 480), framerate=15)
        self.InitializeCamera()
        self.CreaDirectorios(rutaimagenes=self.RutaImagenes, rutacapturas=self.RutaCapturas, rutagifs= self.RutaGifs)

    def LoadJson(self):
        self.data = json.load(open('./config/configuration.json'))

        self.RutaImagenes = self.data["RutaImagenes"]
        self.RutaGifs = self.data["RutaGifs"]
        self.RutaCapturas = self.data["RutaCapturas"]

        self.BOTON_GPIO = self.data["BOTON_GPIO"]
        self.LUZ_BOTON_GPIO = self.data["LUZ_BOTON_GPIO"]
        self.LED_VERDE_GPIO = self.data["LED_VERDE_GPIO"]
        self.LED_NARANJA_GPIO = self.data["LED_NARANJA_GPIO"]
        self.LED_ROJO_GPIO = self.data["LED_ROJO_GPIO"]
        self.FLASH_GPIO = self.data["FLASH_GPIO"]



    def InitializeCamera(self):
        self.Camera.iso = 600
        time.sleep(2)
        self.Camera.shutter_speed = self.Camera.exposure_speed
        self.Camera.shutter_speed = 100000
        self.Camera.exposure_mode = 'off'
        awb_gains = self.Camera.awb_gains
        self.Camera.awb_mode = 'off'
        self.Camera.awb_gains = awb_gains

    ##CreaDirectorios
    def CreaDirectorios(self, rutaimagenes = '../IMAGENES',rutagifs = '../IMAGENES/GIFS', rutacapturas= '../IMAGENES/JPG'):
        self.RutaCapturas = rutacapturas
        self.RutaImagenes = rutaimagenes
        self.RutaGifs = rutagifs

        if not os.path.exists(rutaimagenes):
            os.makedirs(rutaimagenes)
        if not os.path.exists(rutagifs):
            os.makedirs(rutagifs)
        if not os.path.exists(rutacapturas):
            os.makedirs(rutacapturas)
        ##FIN CreaDirectorios