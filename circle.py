import pygame
import time
from musics import Music

pygame.init()

class Circle():
    def __init__(self):
        
        width = 1080
        height = 720

        self.music = Music()

        self.screen = pygame.display.set_mode((width,height))

        self.loadLogo= pygame.transform.scale(pygame.image.load("assets/logop2_3.png"), (720,720))
        self.logoRect = self.loadLogo.get_rect()
        self.logoRect.x = self.screen.get_width() / 6
        self.rotate = None
        self.rotateRadius = 0
        self.screen.blit(self.loadLogo, self.logoRect)
        pygame.display.flip()



    def rotateLogo(self):
        self.music.play("loading",0)
        for i in range(4):
            self.rotateRadius += 90
            self.rotate = pygame.transform.rotate(self.loadLogo, self.rotateRadius)
            self.screen.blit(self.rotate, self.logoRect)
            time.sleep(0.4)
            pygame.display.update()
        