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
        query = """
        SELECT player.id 
        FROM player
        WHERE player.spritepath = %s and player.name = %s
        """
        values = (self.spritePath, self.playerName)
        results = Database.query(query, values)
        PlayerData.playerID = results[0][0]

        # Insert the player data into the database
        query = """
        INSERT INTO playerdata 
        (playerid, health, xp, level, positionx, positiony, currentmap, difficultyid, maxhealth)
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (int(PlayerData.playerID), self.health, self.xp, self.level,
                  self.position[0], self.position[1], self.currentMap, self.difficultyID, self.maxHealth)
        Database.query(query, values)

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
        query = """
        UPDATE playerdata 
        SET health = %s, xp = %s, 
        level = %s, positionx = %s, positiony = %s, 
        currentmap = %s, difficultyid = %s,
        maxhealth = %s
        WHERE playerid = %s"""
        values = (self.health, self.xp, self.level,
                  self.position[0], self.position[1], self.currentMap, self.difficultyID, self.maxHealth, PlayerData.playerID)
        Database.query(query, values)

    @staticmethod
    def upload(player, choice: int):
        """
        update the player data with what's in the database
        """
        query = """SELECT * FROM playerdata WHERE playerdata.playerid = %s"""
        result = Database.query(query, (choice,))[0]
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
        query = """SELECT spritepath FROM player WHERE id = %s"""
        result = Database.query(query, (choice,))[0]
        return result[0]

    @staticmethod
    def setCurrentMap(map):
        """
        Set the map on wich the player should spawn
        """
        query = """SELECT currentmap FROM playerdata WHERE playerid = %s"""
        results = Database.query(query, (PlayerData.playerID,))[0][0]
        map.currentMap = results

    @staticmethod
    def deletePlayer(playerid: int):
        """
        Delete a player from the database
        """

        # delete all the monster of this player
        query = """
        DELETE FROM monstercreated
        USING dungeonplayer
        WHERE dungeonplayer.playerid = %s AND monstercreated.dungeonid = dungeonplayer.id
        """
        Database.query(query, (playerid,))

        # Then delete its dungeon
        query = """
        DELETE FROM dungeonplayer
        WHERE dungeonplayer.playerid = %s
        """

        # And finally delete the player
        Database.query(query, (playerid,))
        query = """DELETE FROM player WHERE id = %s"""
        Database.query(query, (playerid,))
        query = """DELETE FROM playerdata WHERE playerid = %s"""
        Database.query(query, (playerid,))
