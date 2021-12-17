from dataclasses import dataclass
import pygame
from db.db import Database
from db.playerData import PlayerData as Player


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
        # Load the players from the database
        self.players = self.choosePlayer()

        # Load the fonts
        self.titleFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 100)
        self.buttonFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 50)

    def run(self):
        """
        Run the menu, with all its buttons and stuff
        """
        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                # The display changes dipending on the user interaction(load game, quit, etc)
                self.printMenu()
            # Update the display
            pygame.display.update()

        # When the loop is over, return the choice
        return self.choice

    def printMenu(self):
        """
        Print the right menu dependig on the user interaction :
        - Main menu
        - Play menu
        - Options menu
        """

        #### IMAGES ####

        # Load the logo image
        logo = pygame.image.load("./assets/User Interface/logop2_3.png")
        # scale logo down
        logo = pygame.transform.scale(logo, (int(logo.get_width() / 2), int(logo.get_height() / 2)))
        # center logo
        logoRect = logo.get_rect()
        logoRect.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)

        # Load the background image
        background = pygame.image.load("./assets/User Interface/game over 2.png")

        # Display the background image
        self.screen.blit(background, (30, -10))
        self.screen.blit(logo, logoRect)

        # Display the right according to the user choice
        if self.isMainMenuOpen:
            self.mainMenu()
        elif self.isPlayMenuOpen:
            self.playMenu()
        elif self.isOptionsMenuOpen:
            self.optionsMenu()

    @staticmethod
    def clearSurface(surface: pygame.Surface):
        """
        Clear the surface with a black color
        """
        surface.fill((0, 0, 0))

    def playMenu(self):
        """
        Display the play menu, with buttons:
        - Play a new game
        - Play a saved game
        """

        #### TITLE ####
        # Create the title text
        titleText = self.titleFont.render("Choisir une partie", True, (255, 255, 255))
        # center the title text on x-axis
        titleTextRect = titleText.get_rect()
        titleTextRect.centerx = (self.screen.get_width() / 2)
        titleTextRect.centery = 50
        self.screen.blit(titleText, titleTextRect)

        ##### Create a new game button #####
        # Create the new game button text
        newGameButtonText = self.buttonFont.render("Nouvelle Partie", True, (255, 255, 255))
        newGameButtonTextRect = newGameButtonText.get_rect()

        # The background of the button is a rectangle with the size of the text
        bgNewGame = self.createBGSurface(newGameButtonTextRect)
        bgNewGame.blit(newGameButtonText, newGameButtonTextRect)
        bgNewGameRect = bgNewGame.get_rect()

        #### Create different player's save buttons ####

        if len(self.players) > 0:
            for player in self.players:
                # Load the bin image
                binImage = pygame.image.load("./assets/User Interface/poubelle.png")
                # Create the button text
                buttonText = self.buttonFont.render(player.name, True, (255, 255, 255))
                buttonTextRect = buttonText.get_rect()
                bg = self.createBGSurface(buttonTextRect)
                bg.blit(buttonText, buttonTextRect)
                bgRect = bg.get_rect()
                bgRect.height += 20
                bgRect.centerx = (self.screen.get_width() / 2)
                # The button is displayed in the cneter, but offset when there are more buttons
                bgRect.centery = (self.screen.get_height() / 2) + ((bgRect.height * (self.players.index(player) + 1))-((len(self.players)+1)/2*bgRect.height))

                # Get the ratio bewtween the height of the text, and the height of the bin
                scale = binImage.get_height() / buttonTextRect.height
                binImage = pygame.transform.scale(binImage, (binImage.get_width() / scale, buttonTextRect.height))

                #### Create a hover effect ####
                if bgRect.collidepoint(pygame.mouse.get_pos()):
                    # get the mouse click
                    if pygame.mouse.get_pressed()[0]:
                        self.choice = player.id
                        self.running = False
                    # Up the opacity of the bin
                    bg.set_alpha(255)

                # Place the bin on the left of the button
                binImageRect = binImage.get_rect()
                binImageRect.x = bgRect.x - binImageRect.width - 10
                binImageRect.y = bgRect.y

                # Offset the bin on the left of the button, but at the same height
                self.screen.blit(binImage, binImageRect)
                self.screen.blit(bg, bgRect)

                # Detect if the player click on the bin
                if binImageRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Player.deletePlayer(player.id)
                    self.players = self.choosePlayer()

            # The new game button is displayed at the same x-position of the last button
            # but under the previous button
            bgNewGameRect.centerx = bgRect.centerx
            bgNewGameRect.centery = bgRect.centery + bgNewGameRect.height
        else:
            # If there are no players saved,
            # Center bgNewGameRect
            bgNewGameRect.centerx = (self.screen.get_width() / 2)
            bgNewGameRect.centery = (self.screen.get_height() / 2)

        # Detect if the user click on the new game button
        if bgNewGameRect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.choice = 'new'
                self.running = False
            bgNewGame.set_alpha(255)

        #### Create the back button ####
        backButtonText = self.buttonFont.render("Retour", True, (0, 0, 0))
        backButtonTextRect = backButtonText.get_rect()

        bgBack = self.createBGSurface(backButtonTextRect, color=(255, 255, 255))
        bgBack.blit(backButtonText, backButtonTextRect)
        bgBackRect = bgBack.get_rect()
        bgBackRect.height += 20
        bgBackRect.width += 20
        # The button is offset from the left, but at the bottom of the screen
        bgBackRect.x += 50
        bgBackRect.y = self.screen.get_height() - bgBackRect.height

        # detect click on the back button
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
        """
        Display the main menu, with buttons:
        - Play
        - Options (not implemented)
        - Quit
        """

        #### TITLE ####
        # Create the title text
        titleText = self.titleFont.render("Les AUTRES", True, (255, 255, 255))
        # center the title text on x-axis
        titleTextRect = titleText.get_rect()
        titleTextRect.center = ((self.screen.get_width() / 2), 50)
        self.screen.blit(titleText, titleTextRect)

        #### BUTTONS ####
        # Create the button text
        buttonText1 = self.buttonFont.render("Jouer", True, (255, 255, 255))
        buttonText2 = self.buttonFont.render("Quitter", True, (255, 255, 255))

        buttonText1Rect, buttonText2Rect = buttonText1.get_rect(), buttonText2.get_rect()
        btn1BG = self.createBGSurface(buttonText1Rect, offset=50, color=(0, 0, 0))
        btn2BG = self.createBGSurface(buttonText2Rect, offset=50, color=(0, 0, 0))

        btn1BGRect = btn1BG.get_rect()
        btn2BGRect = btn2BG.get_rect()

        # Position the buttons bg
        btn1BGRect.x = 100
        btn1BGRect.y = 200
        btn2BGRect.x = 100
        btn2BGRect.y = 400

        # Center the text on the backgroud
        buttonText1Rect.center = (btn1BGRect.width/2, btn1BGRect.height/2)
        buttonText2Rect.center = (btn2BGRect.width/2, btn2BGRect.height/2)

        mouse = pygame.mouse.get_pos()

        # Add hover effects on hover
        if btn1BGRect.collidepoint(mouse):
            btn1BG.set_alpha(255)
            if pygame.mouse.get_pressed()[0]:
                self.isPlayMenuOpen = True
                self.isMainMenuOpen = False

        if btn2BGRect.collidepoint(mouse):
            btn2BG.set_alpha(255)
            if pygame.mouse.get_pressed()[0]:
                self.running = False

        btn2BG.blit(buttonText2, buttonText2Rect)
        btn1BG.blit(buttonText1, buttonText1Rect)
        self.screen.blit(btn1BG, btn1BGRect)
        self.screen.blit(btn2BG, btn2BGRect)

        if buttonText2Rect.collidepoint(mouse) or buttonText1Rect.collidepoint(mouse):
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    @ staticmethod
    def createBGSurface(text: pygame.Rect, offset: int = 10, color: tuple[int] = (0, 0, 0)) -> pygame.Surface:
        """
        Create a background surface for a given rect (text)
        """
        bgBack = pygame.Surface((text.width + offset, text.height + offset))
        bgBack.fill(color)
        bgBack.set_alpha(200)
        return bgBack

    @ staticmethod
    def choosePlayer() -> list[PlayerData]:
        """
        Load the players from the database
        """

        results = Database.query("SELECT * FROM player")
        players = []
        if len(results) >= 1:
            for result in results:
                players.append(PlayerData(result[0], result[2], result[1], result[3]))

        return players
