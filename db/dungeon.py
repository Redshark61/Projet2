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

        query = """SELECT id FROM WORLD WHERE name = %s"""
        id = Database.query(query, (mapName,))[0][0]
        query = """
        INSERT INTO dungeonplayer (dungeonid, playerid)
        VALUES (%s, %s)
        """
        Database.query(query, (id, PlayerData.playerID))

    @classmethod
    def getDungeons(cls):
        """
        Get all the dungeons for this player
        """
        query = "SELECT * FROM dungeon WHERE playerid = %s"
        return Database.query(query, (PlayerData.playerID,))

    @staticmethod
    def addMonsters(monster) -> int:
        """
        Add the monster to the current dungeon
        """
        result = Database.getLastID(("dungeonplayer"))
        id = Monster.addMonster(result, monster)
        return id

    @classmethod
    def getMonsters(cls, dungeonSpritePath: str) -> tuple[list[tuple], int]:
        """
        Get all the monsters for this dungeon
        """
        # Get the id of the current dungeon
        query = """
        SELECT dungeonplayer.id FROM dungeonplayer 
        INNER JOIN world ON dungeonplayer.dungeonid = world.id
        WHERE world.name = %s AND dungeonplayer.playerid = %s
        """
        dungeonID = Database.query(
            query, (dungeonSpritePath, PlayerData.playerID))[0][0]

        query = """SELECT * FROM monstercreated WHERE dungeonid = %s"""
        results = Database.query(query, (dungeonID,))
        monsterNumber = len(results)
        return results, monsterNumber


    @classmethod
    def getNumberOfWorlds(cls):
        query = f"""
        SELECT * FROM world 
        WHERE isdungeon = false
        """
        results = Database.query(query)[0][0]
        worldNumber = results
        return results, worldNumber
