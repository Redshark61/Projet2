from db.db import Database
from db.monster import Monster
from db.playerData import PlayerData


class Dungeon:

    player = None

    @classmethod
    def addPlayer(cls, player):
        cls.player = player

    @classmethod
    def addDungeon(cls, mapName):
        query = f"INSERT INTO dungeon (dungeonpath, playerid) VALUES ('{mapName}', '{PlayerData.playerID}')"
        Database.query(query)

    @classmethod
    def getDungeons(cls):
        query = f"SELECT * FROM dungeon WHERE playerid = '{PlayerData.playerID}'"
        return Database.query(query)

    @classmethod
    def addMonsters(cls, mapName, index, monster):
        playerID = PlayerData.playerID
        # Get the dungeon id from the playerID
        query = f"SELECT * FROM dungeon WHERE playerid = '{playerID}'"
        results = Database.query(query)
        for dungeon in results:
            if dungeon[1] == mapName:
                Monster.addMonster(dungeon[0], monster, index)

    @classmethod
    def updateMonster(cls):
        playerID = PlayerData.playerID
        # Get the dungeon id from the playerID
        query = f"SELECT * FROM dungeon WHERE playerid = '{playerID}'"
        results = Database.query(query)
        for dungeon in results:
            query = f"SELECT * FROM monster WHERE dungeonid = '{dungeon[0]}'"
            monsters = Database.query(query)
            for monster in monsters:
                query = f"""
                UPDATE monster 
                SET alive = '0' WHERE id = '{monster[0]}'"""
                Database.query(query)

    @classmethod
    def getMonster(cls, dungeonSpritePath):
        # Get the dungeonID from the database based on the sprite path
        query = f""" SELECT id FROM dungeon WHERE dungeonpath = '{dungeonSpritePath}' AND playerid = '{PlayerData.playerID}'"""
        dungeonID = Database.query(query)[0][0]
        query = f"""SELECT * FROM monster WHERE dungeonid = {dungeonID}"""
        results = Database.query(query)
        monsterNumber = len(results)
        return results, monsterNumber
