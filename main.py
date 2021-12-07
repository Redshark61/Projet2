import pygame
from game import Game
from db.difficulty import Difficulty
from db.db import Database


def main():
    # Begining of the game
    db = Database()
    db.connect('projet2')
    results = db.query("SELECT * FROM difficulty")
    for result in results:
        Difficulty(result)

    pygame.init()
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
