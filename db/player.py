import time

from db.db import Database


class Player:
    """
    Add the player save to the database
    """

    def __init__(self, playerData):
        self.playerData = playerData
        self.spritePath = self.playerData.spritePath
        self.name = self.playerData.playerName
        self.creationDate = time.strftime("%d/%m/%Y %H:%M:%S")

    def addNewPlayer(self):
        """
        Add the player save into the database
        """
        self.addPlayer()

    def __str__(self) -> str:
        return "Player: " + self.name + " created on " + self.creationDate

    def addPlayer(self):
        """
        Add the player save into the database
        """
        query = f"""INSERT INTO player (spritepath, name) VALUES ('{self.spritePath}', '{self.name}')"""
        Database.query(query)
