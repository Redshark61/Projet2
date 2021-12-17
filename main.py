import pygame
from game import Game
from menu import Menu
from musics import Music


def main():

    # Begining of the game
    pygame.init()
    # Change the icon of the game
    icon = pygame.image.load("./assets/User Interface/logop2_3.png")
    pygame.display.set_icon(icon)

    # Set up the music
    menuMusic = Music()

    # Initalize the screen but not the variables yet
    game = Game()

    # Display the menu
    menu = Menu(game.screen)

    # Play indefinitely the menu music
    menuMusic.playIfReady("menuMusic", -1)
    menuMusic.setVolume(0.05)

    # Run the menu
    choice = menu.run()

    if choice is None:
        return
    menuMusic.stopMusic()
    game.initalize(choice)

    game.run()


if __name__ == "__main__":
    main()
