from util.logger import clienteLog

class pygame(object):
    dummy = ""
    def pygame(self):
        self.dummy = "vacio"

class PiCamera(object):
    dummy = ""
    def camera(self):
        self.dummy = "vacio"

class emulatorGPIO(object):
    BCM = "BCM"
    BOARD = "BOARD"
    OUT = "OUT"
    IN = "IN"
    LOW = 0
    HIGH = 1
    Loggger = None

    def __init__(self):
        cliente = clienteLog()
        self.Logger = cliente.InicializaLogConsole()

    def setmode(self,a):
        self.Logger.debug(a)

    def setup(self,a, b):
        self.Logger.debug(str(a) + "=" + str(b))

    def output(self,a, b):
        self.Logger.debug(str(a) + "=" + str(b))

    def cleanup(self):
        self.Logger.debug("Clean UP")

    def setmode(self,a):
        self.Logger.debug(a)

    def setwarnings(self,flag):
        self.Logger.debug('False')

    def input(self,flag):
        from random import randint
        aleatorio = randint(0, 5000)
        if( aleatorio%2 == 0 ):
            return True
        else:
            return False