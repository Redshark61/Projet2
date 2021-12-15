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

    menuMusic = Music()
    game = Game()
    menu = Menu(game.screen)
    menuMusic.playIfReady("menuMusic", -1)
    choice = menu.run()

    if choice is None:
        return
    menuMusic.stopMusic()
    game.initalize(choice)

    game.run()


if __name__ == "__main__":
    main()
