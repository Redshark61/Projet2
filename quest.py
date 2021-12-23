import time
import pygame
from db.dungeon import Dungeon
import Variables as variables


class Quest:

    index = 1
    isHidden = False
    questList = []

    def __init__(self, name: str, screen):
        _, numberOfEnemies = Dungeon.getMonsters(name)
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
        self.textNumberEnemies = self.font.render(
            str(self.numberOfEnemies), True, (0, 0, 0))
        Quest.questList.append(self)

    @classmethod
    def setIndex(cls):
        """
        Set the index of the quest in order to position it on the screen
        """
        cls.index += 1

    def drawQuestRect(self):
        #### Setting the sizes ####
        screenWidth = self.screen.get_width()
        x, y = screenWidth - self.width, ((self.index-1) * self.height)

        #### Drawing the quest rectangle ####
        self.surface.set_alpha(200)
        self.surface.fill((120, 120, 120))
        self.surface.blit(self.textName, (10, 0))
        self.surface.blit(self.textNumberEnemies, (10, 40))

        #### Draw the progress bar of enemies left ####
        maxWidth = 200
        try:
            width = (self.numberOfEnemies /
                     self.originalNumberOfEnemies) * maxWidth
        except ZeroDivisionError:
            width = 0
        pygame.draw.rect(self.surface, (0, 0, 0), (35, 53, width, 10))

        # don't draw the first line
        if self.index != 1:
            pygame.draw.line(self.surface, (60, 60, 60),
                             (10, 0), (self.width-10, 0), 2)

        self.screen.blit(self.surface, (x, y))

    def updateNumberOfMonster(self, number: int):
        """
        Updte the number of enemies left
        """
        self.numberOfEnemies = number
        self.textNumberEnemies = self.font.render(
            str(self.numberOfEnemies), True, (0, 0, 0))

    @staticmethod
    def winText():
        """
        display "you won" in the center of the screen in 60px font for 5seconds
        """

        font = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 60)
        text = font.render("You won", True, (0, 255, 0))
        variables.screen.blit(text, (variables.screen.get_width(
        )/2 - text.get_width()/2, variables.screen.get_height()/2 - text.get_height()/2))
        # pygame.display.update()

    def tryToDrawnQuestPanel(self):
        """
        Draw the quest panel if the quest is not hidden
        """
        if not Quest.isHidden:
            self.drawQuestRect()

    @classmethod
    def hideQuestPanel(cls):
        """
        Toggle the quest panel
        """
        cls.isHidden = not cls.isHidden
