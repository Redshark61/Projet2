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
        query = f"""SELECT id FROM WORLD WHERE name = '{mapName}'"""
        id = Database.query(query)[0][0]
        query = f"""
        INSERT INTO dungeonplayer (dungeonid, playerid) VALUES ('{id}', '{PlayerData.playerID}')
        """
        Database.query(query)

    @classmethod
    def getDungeons(cls):
        query = f"SELECT * FROM dungeon WHERE playerid = '{PlayerData.playerID}'"
        return Database.query(query)

    @staticmethod
    def addMonsters(monster):
        result = Database.getLastID("dungeonplayer")
        id = Monster.addMonster(result, monster)
        return id

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
    def getMonsters(cls, dungeonSpritePath):
        # Get the dungeonID from the database based on the sprite path
        query = f"""
        SELECT dungeonplayer.id FROM dungeonplayer 
        INNER JOIN world ON dungeonplayer.dungeonid = world.id
        WHERE world.name = '{dungeonSpritePath}' AND dungeonplayer.playerid = '{PlayerData.playerID}'
        """
        dungeonID = Database.query(query)[0][0]
        query = f"""SELECT * FROM monstercreated WHERE dungeonid = {dungeonID}"""
        results = Database.query(query)
        monsterNumber = len(results)
        return results, monsterNumber
