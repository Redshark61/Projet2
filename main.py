import pygame
from game import Game
from menu import Menu


def main():
    # Begining of the game
    pygame.init()
    # Change the icon of the game
    icon = pygame.image.load("./assets/User Interface/logop2_3.png")
    pygame.display.set_icon(icon)
    game = Game()
    menu = Menu(game.screen)
    choice = menu.run()
    if choice is None:
        return
    game.initalize(choice)

    game.run()


if __name__ == "__main__":
    main()
