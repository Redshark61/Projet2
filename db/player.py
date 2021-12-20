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
        self.difficultyID = self.playerData.difficultyID
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
        query = """INSERT INTO player (spritepath, name, difficultyid) VALUES (%s, %s, %s)"""
        values = (self.spritePath, self.name, self.difficultyID)
        Database.query(query, values)
