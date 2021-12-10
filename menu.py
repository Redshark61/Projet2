import pygame

from db.db import Database
from db.difficulty import Difficulty


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.choice = None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pressedPrintMenu = self.printMenu()
            running = pressedPrintMenu if pressedPrintMenu is not None else True
            pygame.display.update()
        return self.choice

    def printMenu(self):
        #### IMAGES ####
        # Load the menu image
        menuImage1 = pygame.image.load("./assets/User Interface/logop2_3.png")
        # scale menuImage1 down
        menuImage1 = pygame.transform.scale(menuImage1, (int(menuImage1.get_width() / 2), int(menuImage1.get_height() / 2)))
        # center menuImage1
        menuImage1Rect = menuImage1.get_rect()
        menuImage1Rect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        menuImage2 = pygame.image.load("./assets/User Interface/game over 2.png")
        self.screen.blit(menuImage2, (30, -10))
        self.screen.blit(menuImage1, menuImage1Rect)

        #### TITLE ####
        # Load the title font
        titleFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 100)
        # Create the title text
        titleText = titleFont.render("Les AUTRES", True, (255, 255, 255))
        # center the title text on x-axis
        titleTextRect = titleText.get_rect()
        titleTextRect.centerx = (self.screen.get_width() / 2)
        titleTextRect.centery = 50
        # blit the title text
        self.screen.blit(titleText, titleTextRect)

        #### BUTTONS ####

        # Load the button font
        buttonFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 50)
        # Create the button text
        buttonText1 = buttonFont.render("Jouer", True, (255, 255, 255))
        buttonText2 = buttonFont.render("Quitter", True, (255, 255, 255))
        # center the button text on x-axis
        buttonText1Rect = buttonText1.get_rect()
        buttonText2Rect = buttonText2.get_rect()
        buttonText1Rect.x += 100
        buttonText1Rect.centery = self.screen.get_height() / 2 - 100

        buttonText2Rect.x += 100
        buttonText2Rect.centery = self.screen.get_height() / 2 + 100

        # blit the button text
        self.screen.blit(buttonText1, buttonText1Rect)
        self.screen.blit(buttonText2, buttonText2Rect)

        # Change buttons color on hover
        mouse = pygame.mouse.get_pos()
        # set the rect larger than the button text
        button1Rect = pygame.Rect(buttonText1Rect.x - 10, buttonText1Rect.y - 10, buttonText1Rect.width + 20, buttonText1Rect.height + 20)
        button2Rect = pygame.Rect(buttonText2Rect.x - 10, buttonText2Rect.y - 10, buttonText2Rect.width + 20, buttonText2Rect.height + 20)

        if buttonText1Rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, (255, 255, 255), button1Rect, 2, border_radius=20)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), button1Rect, 2, border_radius=20)

        if buttonText2Rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, (255, 255, 255), button2Rect, 2, border_radius=20)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), button2Rect, 2, border_radius=20)

        if buttonText2Rect.collidepoint(mouse) or buttonText1Rect.collidepoint(mouse):
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)

        # Get the mouse click on the quit button
        if buttonText2Rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            return False

        if buttonText1Rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            self.choice = self.choosePlayer()
            return False

    @staticmethod
    def choosePlayer():
        db = Database()
        db.connect('projet2')
        results = db.query("SELECT * FROM difficulty")
        for result in results:
            Difficulty(result)
        choice = None
        results = db.query("SELECT * FROM player")

        if len(results) >= 1:
            print(f"{len(results)} players, wich one do you want to play with?")
            for index, result in enumerate(results):
                print(f"{index} - {result[2]}")
            print(f"{len(results)} - New player")
            choice = int(input(""))

            if choice == len(results):
                choice = 'new'
            return choice
        else:
            return 'new'
