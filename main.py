import pygame
from game import Game


def main():
    # Begining of the game
    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
