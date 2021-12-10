import pygame
import time

pygame.init()

class Circle():
    def __init__(self):
        
        width = 1080
        height = 720

        self.screen = pygame.display.set_mode((width,height))

        self.loadLogo= pygame.transform.scale(pygame.image.load("assets/logop2_3.png"), (720,720))
        self.logoRect = self.loadLogo.get_rect()
        self.logoRect.x = self.screen.get_width() / 6
        self.rotate = None
        self.rotateRadius = 0
        self.screen.blit(self.loadLogo, self.logoRect)
        pygame.display.flip()



    # def circlePass(self):
    #     for i in range(1,23):
    #         self.circleScale -= 400
    #         self.circleBlitScale += 200
    #         self.circle = pygame.transform.scale(self.loadCircle,(self.circleScale + 400,self.circleScale + 200))
            
    #         # self.circleList.append(self.circle)
    #         self.screen.blit(self.circle, (self.circleBlitScale,self.circleBlitScale))
    #         time.sleep(0.05)
    #         pygame.display.update()
    #     self.backgroundEnd.fill(self.black)
    #     self.screen.blit(self.backgroundEnd,(0,0))
    #     pygame.display.update()
    def rotateLogo(self):
        for i in range(4):
            self.rotateRadius += 90
            self.rotate = pygame.transform.rotate(self.loadLogo, self.rotateRadius)
            self.screen.blit(self.rotate, self.logoRect)
            time.sleep(0.5)
            pygame.display.update()
    # def runningCircle(self):

    #     running = True
    #     while running:

    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYDOWN:
    #                 running = False
    #             button_down = pygame.mouse.get_pressed()
    #             if button_down[0]:
    #                 print("Clicked")
    #                 runCircle = Circle()
    #                 runCircle.circlePass()
                    
                  
    #     pygame.quit()

    
# run = Circle()
# run.runningCircle()