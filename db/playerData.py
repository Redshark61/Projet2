from db.db import Database
from db.player import Player
from db.difficulty import Difficulty


class PlayerData:

    modelList = []

    def __init__(self, player):
        self.player = player
        self.health = self.player.health
        self.xp = self.player.totalXP
        self.level = self.player.currentLevel
        self.position = (self.player.rect.x, self.player.rect.y)
        self.currentMap = self.player.map
        self.difficultyID = 1
        self.playerName = self.player.playerName
        self.spritePath = self.player.name
        self.difficultyName = [difficulty.name for difficulty in Difficulty.modelList if difficulty.ID == self.difficultyID][0]
        PlayerData.modelList.append(self)
        Player(self)
        self.addPlayer()

    def __str__(self) -> str:
        return f"{self.playerName=} - {self.health=} - {self.xp=} - {self.level=} - {self.position=} - {self.currentMap=} - {self.difficultyName=} - {self.spritePath=}"

    def addPlayer(self):
        results = Database.query(f"""
        SELECT player.id FROM player WHERE player.spritepath = '{self.spritePath}'
        """)
        print(results)
        playerID = results[0][0]
        # playerID = [player.id for player in Player.modelList if player.playerName == self.playerName][0]
        query = f"""INSERT INTO playerdata (playerid, health, xp, level, positionx, positiony, currentmap, difficultyid)
                    VALUES ('{int(playerID)}','{self.health}', '{self.xp}', '{self.level}', '{self.position[0]}', '{self.position[1]}', '{self.currentMap}', '{self.difficultyID}')"""
        Database.query(query)
