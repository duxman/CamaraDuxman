#https://learn.adafruit.com/using-a-mini-pal-ntsc-display-with-a-raspberry-pi/configure-and-test
#https://learn.adafruit.com/pi-video-output-using-pygame/pointing-pygame-to-the-framebuffer
import os
import pygame
import time
import random
 
class pygameScreen :
    Logger = None
    screen = None

    def initializeRpI(self):
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
            exit(1)

        os.putenv('SDL_VIDEODRIVER', 'fbcon')
        os.putenv("SDL_FBDEV", '/dev/fb0')

        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                self.Logger.error ('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break

        if not found:
            self.Logger.error('No suitable video driver found!')
            raise Exception('No suitable video driver found!')

    def initializeWin(self):
        initialize = ""

    def __init__(self,logger):
        self.Logger = logger

        if os.name == 'poxis':
            self.initializeRpI();
        else:
            pygame.display.init()

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 255, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

        

 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."         
 
    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 0, 0)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()
