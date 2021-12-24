import pygame
from game import Game
from menu import Menu
from musics import Music
from quest import Quest
import Variables as variables


def main():

    # Begining of the game
    pygame.init()
    # Change the icon of the game
    icon = pygame.image.load("./assets/User Interface/logop2_3.png")
    pygame.display.set_icon(icon)

    again = True
    game = Game()
    variables.game = game
    startNewGame = False
    while again:

        Quest.index = 1
        # Set up the music
        menuMusic = Music(again)
        # again = False
        # Initalize the screen but not the variables yet

        # Display the menu
        menu = Menu()

        # Play indefinitely the menu music
        menuMusic.playIfReady("menuMusic", -1)

        # Run the menu
        choice, difficulty, name = menu.run()

        if choice is None:
            return
        menuMusic.stopMusic()
        game.initalize(choice, difficulty, name)

        again = game.run(startNewGame)
        startNewGame = again


if __name__ == "__main__":
    main()
