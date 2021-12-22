import sys
from dataclasses import dataclass
import pygame
from db.db import Database
from db.playerData import PlayerData as Player
import utilities.pygameMenu as util
import Variables as variables


@dataclass
class PlayerData:
    id: int
    name: str
    spritepath: str
    creationDate: str


class Menu:
    # Only initialize the font and the main variables
    pygame.font.init()
    running = True
    # Set all the states
    isPlayMenuOpen = False
    isMainMenuOpen = True
    isOptionsMenuOpen = False
    isDifficultyMenuOpen = False
    isNameMenuOpen = False

    # Load the fonts
    titleFont = pygame.font.Font("./assets/font/Shadowed.ttf", 60)
    buttonFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 50)

    # User input specific variables
    userText = ''
    active = False
    pressedOnce = False

    def __init__(self):
        # variables.screen = screen
        Menu.isMainMenuOpen = True
        Menu.running = True
        self.choice = None
        self.difficulty = None
        self.difficulties = Database.query("SELECT * FROM difficulty ORDER BY id")

        # Load the players from the database
        self.players = self.choosePlayer()

    def run(self) -> tuple[str, int]:
        """
        Run the menu, with all its buttons and stuff
        """
        while Menu.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    Menu.running = False
                    pygame.quit()
                    sys.exit()

                # The display changes dipending on the user interaction(load game, quit, etc)
                self.printMenu()
            # Update the display
            pygame.display.update()

        # When the loop is over, return the choice
        return self.choice, self.difficulty, Menu.userText

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
        logoRect.center = (variables.screen.get_width() / 2, variables.screen.get_height() / 2)

        # Load the background image
        background = pygame.image.load("./assets/User Interface/game over 2.png")

        # Display the background image
        variables.screen.blit(background, (30, -10))
        variables.screen.blit(logo, logoRect)

        # Display the right according to the user choice
        if Menu.isMainMenuOpen:
            self.mainMenu()
        elif Menu.isPlayMenuOpen:
            self.playMenu()
        elif Menu.isOptionsMenuOpen:
            self.optionsMenu()
        elif Menu.isDifficultyMenuOpen:
            self.difficultyMenu()
        elif Menu.isNameMenuOpen:
            self.nameMenu()

    @staticmethod
    def nameMenu():
        # Create the back button
        Menu.isNameMenuOpen, Menu.isDifficultyMenuOpen = util.createButton(
            variables.screen, Menu.isNameMenuOpen, Menu.isDifficultyMenuOpen, "Retour")

        Menu.isNameMenuOpen, _ = util.createButton(
            variables.screen, Menu.isNameMenuOpen, Menu.active, "Suivant", position='br', name="menu.Menu.running", value=False)
        activeColor = (0, 0, 0)
        passiveColor = (100, 100, 100)
        # Create the text input
        util.textInput(variables.screen, activeColor, passiveColor)

    def difficultyMenu(self):
        """
        Display the difficulty menu
        """

        # get the difficulties from the database

        #### TITLE ####
        Menu.titleFont.render("Difficulty", True, (255, 255, 255))

        #### BUTTONS ####
        # Create the buttons for each difficulty
        for _, difficulty in enumerate(self.difficulties):
            # Colors are the last three colomns from the database
            r, g, b = difficulty[-3:]
            button = Menu.buttonFont.render(difficulty[1], True, (255, 255, 255))
            buttonRect = button.get_rect()
            buttonRect.height += 20
            buttonRect.x = 100
            # The button is displayed in the cneter, but offset when there are more buttons
            buttonRect.centery = (variables.screen.get_height() / 2) + ((buttonRect.height *
                                                                         (self.difficulties.index(difficulty) + 1))-((len(self.difficulties)+1)/2*buttonRect.height))

            # If the mouse is on a difficulty button, change the color
            if buttonRect.collidepoint(pygame.mouse.get_pos()):
                button = Menu.buttonFont.render(difficulty[1], True, (int(r), int(g), int(b)))
                # Detect the click on the button
                if pygame.mouse.get_pressed()[0]:
                    Menu.isDifficultyMenuOpen = False
                    Menu.isNameMenuOpen = True
                    self.choice = 'new'
                    self.difficulty = difficulty[0]

            # Create a back button
            Menu.isDifficultyMenuOpen, Menu.isMainMenuOpen = util.createButton(
                variables.screen, Menu.isDifficultyMenuOpen, Menu.isMainMenuOpen, "Retour")
            variables.screen.blit(button, buttonRect)

    def playMenu(self):
        """
        Display the play menu, with buttons:
        - Play a new game
        - Play a saved game
        """

        #### TITLE ####
        # Create the title text
        titleText = Menu.titleFont.render(
            "Choisir une partie", True, (255, 255, 255))
        # center the title text on x-axis
        titleTextRect = titleText.get_rect()
        titleTextRect.center = ((variables.screen.get_width() / 2), 50)
        variables.screen.blit(titleText, titleTextRect)

        ##### Create a new game button #####
        # Create the new game button text
        newGameButtonText = Menu.buttonFont.render(
            "Nouvelle Partie", True, (255, 255, 255))
        newGameButtonTextRect = newGameButtonText.get_rect()

        # The background of the button is a rectangle with the size of the text
        bgNewGame = util.createBGSurface(newGameButtonTextRect)
        bgNewGame.blit(newGameButtonText, newGameButtonTextRect)
        bgNewGameRect = bgNewGame.get_rect()

        #### Create different player's save buttons ####

        if len(self.players) > 0:
            for player in self.players:
                # Load the bin image
                binImage = pygame.image.load("./assets/User Interface/poubelle.png")
                # Create the button text
                buttonText = Menu.buttonFont.render(player.name, True, (255, 255, 255))
                buttonTextRect = buttonText.get_rect()
                bg = util.createBGSurface(buttonTextRect)
                bg.blit(buttonText, buttonTextRect)
                bgRect = bg.get_rect()
                bgRect.height += 20
                bgRect.centerx = (variables.screen.get_width() / 2)
                # The button is displayed in the cneter, but offset when there are more buttons
                bgRect.centery = (variables.screen.get_height() / 2) + ((bgRect.height *
                                                                         (self.players.index(player) + 1))-((len(self.players)+1)/2*bgRect.height))

                # Get the ratio bewtween the height of the text, and the height of the bin
                scale = binImage.get_height() / buttonTextRect.height
                binImage = pygame.transform.scale(
                    binImage, (binImage.get_width() / scale, buttonTextRect.height))

                #### Create a hover effect ####
                if bgRect.collidepoint(pygame.mouse.get_pos()):
                    # get the mouse click
                    if pygame.mouse.get_pressed()[0]:
                        self.choice = player.id
                        Menu.running = False
                    # Up the opacity of the bin
                    bg.set_alpha(255)

                # Place the bin on the left of the button
                binImageRect = binImage.get_rect()
                binImageRect.x, binImageRect.y = (bgRect.x - binImageRect.width - 10), bgRect.y

                # Offset the bin on the left of the button, but at the same height
                variables.screen.blit(binImage, binImageRect)
                variables.screen.blit(bg, bgRect)

                # Detect if the player click on the bin
                if binImageRect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                    Player.deletePlayer(player.id)
                    self.players = self.choosePlayer()

            # The new game button is displayed at the same x-position of the last button
            # but under the previous button
            bgNewGameRect.center = (bgRect.centerx, (bgRect.centery + bgNewGameRect.height))
        else:
            # If there are no players saved,
            # Center bgNewGameRect
            bgNewGameRect.center = ((variables.screen.get_width() / 2), (variables.screen.get_height() / 2))

        # Detect if the user click on the new game button
        if bgNewGameRect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                Menu.isPlayMenuOpen = False
                Menu.isDifficultyMenuOpen = True
            bgNewGame.set_alpha(255)

        #### Create the back button ####

        Menu.isPlayMenuOpen, Menu.isMainMenuOpen = util.createButton(
            variables.screen, Menu.isPlayMenuOpen, Menu.isMainMenuOpen, "Retour")
        variables.screen.blit(bgNewGame, bgNewGameRect)

    def mainMenu(self):
        """
        Display the main menu, with buttons:
        - Play
        - Options (not implemented)
        - Quit
        """

        #### TITLE ####
        # Create the title text
        titleText = Menu.titleFont.render("The Night Monsters Fever", True, (245, 159, 34))
        # center the title text on x-axis
        titleTextRect = titleText.get_rect()
        titleTextRect.center = ((variables.screen.get_width() / 2), 50)
        variables.screen.blit(titleText, titleTextRect)

        #### BUTTONS ####
        # Create the button text
        buttonText1 = Menu.buttonFont.render("Jouer", True, (245, 159, 34))
        buttonText2 = Menu.buttonFont.render("Quitter", True, (245, 159, 34))

        buttonText1Rect, buttonText2Rect = buttonText1.get_rect(), buttonText2.get_rect()

        btn1BG = util.createBGSurface(
            buttonText1Rect, offset=00, color=(0, 0, 0))
        btn2BG = util.createBGSurface(
            buttonText2Rect, offset=00, color=(0, 0, 0))

        btn1BGRect = btn1BG.get_rect()
        btn2BGRect = btn2BG.get_rect()


        # Position the buttons bg
        buttonText1Rect.x = 100
        buttonText1Rect.y = 200
        buttonText2Rect.x = 100
        buttonText2Rect.y = 400

        mouse = pygame.mouse.get_pos()

        # Add hover effects on hover
        if buttonText1Rect.collidepoint(mouse):
            buttonText1.set_alpha(255)
            if pygame.mouse.get_pressed()[0]:
                Menu.isPlayMenuOpen = True
                Menu.isMainMenuOpen = False

        if buttonText2Rect.collidepoint(mouse):
            buttonText2.set_alpha(255)
            if pygame.mouse.get_pressed()[0]:
                Menu.running = False

        variables.screen.blit(buttonText1, buttonText1Rect)
        variables.screen.blit(buttonText2, buttonText2Rect)

        if buttonText2Rect.collidepoint(mouse) or buttonText1Rect.collidepoint(mouse):
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    @ staticmethod
    def choosePlayer() -> list[PlayerData]:
        """
        Load the players from the database
        """

        results = Database.query("SELECT * FROM player")
        players = []
        if len(results) >= 1:
            for result in results:
                players.append(PlayerData(
                    result[0], result[2], result[1], result[3]))

        return players

    @staticmethod
    def drawDeathMenu():
        running = True
        # Set the clock to 60fps
        clock = pygame.time.Clock()
        while running:
            # If the player is dead, display the death scene
            background = pygame.image.load('assets/Background Game Over.png')
            background2 = pygame.Surface(variables.screen.get_size())
            background2.fill((0, 0, 0))
            banner = pygame.image.load('assets/Banner Game Over.png')
            quitButton = Menu.buttonFont.render("Quitter", True, (255, 255, 255))
            returnButton = Menu.buttonFont.render("Retour", True, (255, 255, 255))
            quitButtonRect = quitButton.get_rect()
            quitButtonRect.x, quitButtonRect.y = 800, 600
            returnButtonRect = returnButton.get_rect()
            returnButtonRect.x, returnButtonRect.y = 100, 600
            variables.screen.blit(background2, (0, 0))
            variables.screen.blit(background, (30, 0))
            variables.screen.blit(banner, (280, 50))
            variables.screen.blit(quitButton, quitButtonRect)
            variables.screen.blit(returnButton, returnButtonRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quitButtonRect.collidepoint(pygame.mouse.get_pos()):
                        return False
                    if returnButtonRect.collidepoint(pygame.mouse.get_pos()):
                        return True

            pygame.display.update()
            pygame.display.flip()
            clock.tick(60)

        pygame.display.quit()
