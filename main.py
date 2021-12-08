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
    choice = None
    results = db.query("SELECT * FROM player")

    if len(results) >= 1:
        print(f"{len(results)} players, wich one do you want to play with?")
        for index, result in enumerate(results):
            print(f"{index} - {result[2]}")
        print(f"{len(results)} - New player")
        choice = int(input(""))

        if choice == len(results):
            choice = None

    pygame.init()
    game = Game(choice)
    game.run()


if __name__ == "__main__":
    main()
