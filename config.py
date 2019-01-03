import os
import time
from CameraExtraGrafica import pyscope

if os.name == 'poxis':
    import picamera.PiCamera as PiCamera
else:
    from emulators.emulators import PiCamera


class config(object):

    Pantalla = None
    Camera = None
    RutaImagenes = '../IMAGENES'
    RutaGifs = '../IMAGENES/GIFS'
    RutaCapturas = '../IMAGENES/JPG'

    def __init__(self):
        self.Pantalla = pyscope();
        self.Camera = PiCamera(resolution=(640, 480), framerate=15)
        self.InitializeCamera()
        self.CreaDirectorios()

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