from db.db import Database
from db.player import Player


class PlayerData:

    playerID = None

    def __init__(self, player):
        self.player = player
        self.updateValue()
        self.playerDB = Player(self)

    def addToList(self):
        """
        Add the player into the database
        """
        self.playerDB.addNewPlayer()
        self.addPlayer()

    def addPlayer(self):
        """
        Add the player into the database
        """
        # Get the player id
        results = Database.query(f"""
        SELECT player.id 
        FROM player
        WHERE player.spritepath = '{self.spritePath}' and player.name = '{self.playerName}'
        """)
        PlayerData.playerID = results[0][0]

        # Insert the player data into the database
        query = f"""
        INSERT INTO playerdata 
        (playerid, health, xp, level, positionx, positiony, currentmap, difficultyid, maxhealth)
        VALUES ('{int(PlayerData.playerID)}','{self.health}', '{self.xp}', '{self.level}', 
        '{self.position[0]}', '{self.position[1]}', '{self.currentMap}', '{self.difficultyID}', 
        '{self.maxHealth}')
        """
        Database.query(query)

    def updateValue(self):
        """
        Get all the value from player data
        """
        self.health = int(self.player.health)
        self.maxHealth = int(self.player.maxHealth)
        self.xp = self.player.totalXP
        self.level = self.player.currentLevel
        self.position = (self.player.rect.x, self.player.rect.y)
        self.currentMap = self.player.map
        self.difficultyID = 1
        self.playerName = self.player.playerName
        self.spritePath = self.player.name

        # If the player already exist in the database, update the value
        if PlayerData.playerID is not None:
            self.updateDB()

    def updateDB(self):
        """
        Update the value of player data into the database
        """
        query = f"""
        UPDATE playerdata 
        SET health = '{self.health}', xp = '{self.xp}', 
        level = '{self.level}', positionx = '{self.position[0]}', positiony = '{self.position[1]}', 
        currentmap = '{self.currentMap}', difficultyid = '{self.difficultyID}',
        maxhealth = '{self.maxHealth}'
        WHERE playerid = '{PlayerData.playerID}'"""
        Database.query(query)

    @staticmethod
    def upload(player, choice: int):
        """
        update the player data with what's in the database
        """
        query = f"""SELECT * FROM playerdata WHERE playerdata.playerid = '{choice}'"""
        result = Database.query(query)[0]
        PlayerData.playerID = result[0]
        player.health = result[1]
        player.totalXP = result[2]
        player.currentLevel = result[3]
        player.rect.x = result[4]
        player.rect.y = result[5]
        player.map = result[6]
        player.maxHealth = result[8]

    @staticmethod
    def getSpritePath(choice: int) -> str:
        """
        Get the sprite path of the player
        """
        query = f"""SELECT spritepath FROM player WHERE id = '{choice}'"""
        result = Database.query(query)[0]
        return result[0]

    @staticmethod
    def setCurrentMap(map):
        """
        Set the map on wich the player should spawn
        """
        query = f"""SELECT currentmap FROM playerdata WHERE playerid = '{PlayerData.playerID}'"""
        results = Database.query(query)[0][0]
        map.currentMap = results

    @staticmethod
    def deletePlayer(playerid: int):
        """
        Delete a player from the database
        """

        # delete all the monster of this player
        query = f"""
        DELETE FROM monstercreated
        USING dungeonplayer
        WHERE dungeonplayer.playerid = '{playerid}' AND monstercreated.dungeonid = dungeonplayer.id
        """
        Database.query(query)

        # Then delete its dungeon
        query = f"""
        DELETE FROM dungeonplayer
        WHERE dungeonplayer.playerid = '{playerid}'
        """

        # And finally delete the player
        Database.query(query)
        query = f"""DELETE FROM player WHERE id = '{playerid}'"""
        Database.query(query)
        query = f"""DELETE FROM playerdata WHERE playerid = '{playerid}'"""
        Database.query(query)
