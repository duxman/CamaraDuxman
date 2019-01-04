import threading

class WriterCaptura(threading.Thread):
    CurrentFrameQueue = None
    Camera = None
    Stop = False

    def __init__(self, queue, camara):
        threading.Thread.__init__(self)
        self.CurrentFrameQueue = queue
        self.Camera = camara

    def run(self):
        while self.Stop == False:
            ret, CurrentFrame = self.Camera.read()
            CurrentFrame.put(CurrentFrame)