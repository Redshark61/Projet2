import time
import pygame


class Quest:

    index = 1
    isHidden = False

    def __init__(self, numberOfEnemies, name, screen):
        self.originalNumberOfEnemies = numberOfEnemies
        self.numberOfEnemies = numberOfEnemies
        self.originalName = name
        self.name = self.originalName.split("/")[0].split("asset")[1]
        self.screen = screen
        self.index = Quest.index
        self.height = 90
        self.width = 300
        # draw the quest rectangle on the right side of the screen
        self.surface = pygame.Surface((self.width, self.height))
        self.setIndex()
        # add the name of the quest to the surface
        self.font = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 20)
        self.textName = self.font.render(self.name, True, (0, 0, 0))

        self.textNumberEnemies = self.font.render(str(self.numberOfEnemies), True, (0, 0, 0))

    @classmethod
    def setIndex(cls):
        cls.index += 1

    def drawQuestRect(self):
        #### Setting the sizes ####
        screenWidth = self.screen.get_width()
        screenHeight = self.screen.get_height()
        x, y = screenWidth - self.width, ((self.index-1) * self.height)

        #### Drawing the quest rectangle ####
        self.surface.set_alpha(200)
        self.surface.fill((120, 120, 120))
        self.surface.blit(self.textName, (10, 0))
        self.surface.blit(self.textNumberEnemies, (10, 40))

        #### Draw the progress bar of enemies left ####
        maxWidth = 200
        width = (self.numberOfEnemies / self.originalNumberOfEnemies) * maxWidth
        pygame.draw.rect(self.surface, (0, 0, 0), (35, 53, width, 10))

        # don't draw the first line
        if self.index != 1:
            pygame.draw.line(self.surface, (60, 60, 60), (10, 0), (self.width-10, 0), 2)

        self.screen.blit(self.surface, (x, y))

    def updateNumberOfMonster(self, number):
        self.numberOfEnemies = number
        self.textNumberEnemies = self.font.render(str(self.numberOfEnemies), True, (0, 0, 0))

    def winText(self):
        # display "you have win" in the center of the screen in 60px font for 5seconds

        font = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 60)
        text = font.render("You have won", True, (0, 255, 0))
        self.screen.blit(text, (self.screen.get_width()/2 - text.get_width()/2, self.screen.get_height()/2 - text.get_height()/2))
        pygame.display.update()

    def tryToDrawnQuestPanel(self):
        if not Quest.isHidden:
            self.drawQuestRect()

    @classmethod
    def hideQuestPanel(cls):
        cls.isHidden = not cls.isHidden
