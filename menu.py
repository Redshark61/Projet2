from dataclasses import dataclass
import pygame
from db.db import Database
from db.difficulty import Difficulty
from db.playerData import PlayerData as Player
from musics import Music

@dataclass
class PlayerData:
    id: int
    name: str
    spritepath: str
    creationDate: str


class Menu:

    def __init__(self, screen):
        self.screen = screen
        self.choice = None
        self.running = True
        self.isPlayMenuOpen = False
        self.isMainMenuOpen = True
        self.isOptionsMenuOpen = False
        self.players = self.choosePlayer()
        self.titleFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 100)
        self.buttonFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 50)
        # Initiliaze music
        self.menuMusic = Music()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.printMenu()
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

        if self.isMainMenuOpen:
            self.mainMenu()
        elif self.isPlayMenuOpen:
            self.playMenu()
        elif self.isOptionsMenuOpen:
            self.optionsMenu()

    @staticmethod
    def clearSurface(surface):
        surface.fill((0, 0, 0))

    def playMenu(self):

        #### TITLE ####
        # Create the title text
        titleText = self.titleFont.render("Choisir une partie", True, (255, 255, 255))
        # center the title text on x-axis
        titleTextRect = titleText.get_rect()
        titleTextRect.centerx = (self.screen.get_width() / 2)
        titleTextRect.centery = 50
        # blit the title text
        self.screen.blit(titleText, titleTextRect)

        #### Create a new game button ####
        # Create the button text
        newGameButtonText = self.buttonFont.render("Nouvelle Partie", True, (255, 255, 255))
        # center the button text on x-axis
        newGameButtonTextRect = newGameButtonText.get_rect()
        bgNewGame = pygame.Surface((newGameButtonTextRect.width + 10, newGameButtonTextRect.height + 10))
        bgNewGame.fill((0, 0, 0))
        bgNewGame.set_alpha(200)
        bgNewGame.blit(newGameButtonText, newGameButtonTextRect)
        bgNewGameRect = bgNewGame.get_rect()

        #### Create different player's save buttons ####

        if len(self.players) > 0:
            for player in self.players:
                # Load the bin image
                binImage = pygame.image.load("./assets/User Interface/poubelle.png")
                # Create the button text
                buttonText = self.buttonFont.render(player.name, True, (255, 255, 255))
                # center the button text on x-axis
                buttonTextRect = buttonText.get_rect()
                scale = binImage.get_height() / buttonTextRect.height
                binImage = pygame.transform.scale(binImage, (binImage.get_width() / scale, buttonTextRect.height))
                bg = pygame.Surface((buttonTextRect.width + 10, buttonTextRect.height + 10))
                bg.fill((0, 0, 0))
                bg.set_alpha(200)
                bg.blit(buttonText, buttonTextRect)
                bgRect = bg.get_rect()
                bgRect.height += 20
                bgRect.centerx = (self.screen.get_width() / 2)
                bgRect.centery = (self.screen.get_height() / 2) + ((bgRect.height * (self.players.index(player) + 1))-((len(self.players)+1)/2*bgRect.height))

                #### Create a hover effect ####
                if bgRect.collidepoint(pygame.mouse.get_pos()):
                    # get the mouse click
                    if pygame.mouse.get_pressed()[0]:
                        self.choice = player.id
                        self.running = False
                    bg.set_alpha(255)

                # Place the bin on the left of the button
                binImageRect = binImage.get_rect()
                binImageRect.x = bgRect.x - binImageRect.width - 10
                binImageRect.y = bgRect.y
                self.screen.blit(binImage, binImageRect)
                self.screen.blit(bg, bgRect)

                # Detect if the player click on the bin
                if binImageRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Player.deletePlayer(player.id)
                    self.players = self.choosePlayer()

            bgNewGameRect.centerx = bgRect.centerx
            bgNewGameRect.centery = bgRect.centery + bgNewGameRect.height
        else:
            # Center bgNewGameRect
            bgNewGameRect.centerx = (self.screen.get_width() / 2)
            bgNewGameRect.centery = (self.screen.get_height() / 2)

        if bgNewGameRect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.choice = 'new'
                self.running = False
            bgNewGame.set_alpha(255)

        #### Create the back button ####
        backButtonText = self.buttonFont.render("Retour", True, (0, 0, 0))
        backButtonTextRect = backButtonText.get_rect()

        bgBack = pygame.Surface((backButtonTextRect.width + 10, backButtonTextRect.height + 10))
        bgBack.fill((255, 255, 255))
        bgBack.set_alpha(200)
        bgBack.blit(backButtonText, backButtonTextRect)
        bgBackRect = bgBack.get_rect()
        bgBackRect.height += 20
        bgBackRect.width += 20
        bgBackRect.x += 50
        bgBackRect.y = self.screen.get_height() - bgBackRect.height

        # hover effect
        if bgBackRect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.clearSurface(self.screen)
                self.isPlayMenuOpen = False
                self.isMainMenuOpen = True
                return
            bgBack.set_alpha(255)

        self.screen.blit(bgBack, bgBackRect)
        self.screen.blit(bgNewGame, bgNewGameRect)
        
    def mainMenu(self):

        #### TITLE ####
        # Create the title text
        titleText = self.titleFont.render("Les AUTRES", True, (255, 255, 255))
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
            self.running = False

        if buttonText1Rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            self.isPlayMenuOpen = True
            self.isMainMenuOpen = False
            # self.choice = self.choosePlayer()
            # self.running = False

    @ staticmethod
    def choosePlayer():
        db = Database()
        db.connect('projet2')

        results = db.query("SELECT * FROM player")
        players = []
        if len(results) >= 1:
            for result in results:
                players.append(PlayerData(result[0], result[2], result[1], result[3]))

        return players
