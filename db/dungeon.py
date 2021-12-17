from db.db import Database
from db.monster import Monster
from db.playerData import PlayerData


class Dungeon:

    player = None

    @classmethod
    def addPlayer(cls, player):
        """
        Create the current player for this dungeon
        """
        cls.player = player

    @classmethod
    def addDungeon(cls, mapName: str):
        """
        Create the current dungeon for this player
        """

        query = f"""SELECT id FROM WORLD WHERE name = '{mapName}'"""
        id = Database.query(query)[0][0]
        query = f"""
        INSERT INTO dungeonplayer (dungeonid, playerid)
        VALUES ('{id}', '{PlayerData.playerID}')
        """
        Database.query(query)

    @classmethod
    def getDungeons(cls):
        """
        Get all the dungeons for this player
        """
        query = f"SELECT * FROM dungeon WHERE playerid = '{PlayerData.playerID}'"
        return Database.query(query)

    @staticmethod
    def addMonsters(monster) -> int:
        """
        Add the monster to the current dungeon
        """
        result = Database.getLastID("dungeonplayer")
        id = Monster.addMonster(result, monster)
        return id

    @classmethod
    def getMonsters(cls, dungeonSpritePath: str) -> tuple[list[tuple], int]:
        """
        Get all the monsters for this dungeon
        """
        # Get the id of the current dungeon
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
