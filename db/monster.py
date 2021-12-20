from db.db import Database
from db.playerData import PlayerData


class Monster:

    @classmethod
    def addMonster(cls, dungeonID: int, monster) -> list[tuple]:
        """
        Add monster into the database
        """
        query = """
        INSERT INTO monstercreated
        (monsterid, positionx, positiony, health, speed, dungeonid) 
        VALUES 
        (%s, %s, %s, %s, %s, %s)
        """
        values = (monster.monsterID, monster.rect.x, monster.rect.y,
                  monster.health, monster.speed, dungeonID)
        Database.query(query, values)
        return Database.getLastID("monstercreated")

    @staticmethod
    def update(monsters):
        """
        Update the value of monster data into the database
        """
        for monster in monsters:
            query = """
            UPDATE monstercreated
            SET positionx = %s, positiony = %s, health = %s
            WHERE id = %s"""
            values = (monster.rect.x, monster.rect.y,
                      monster.health, monster.index)
            Database.query(query, values)

    @staticmethod
    def getAllMonster() -> list[tuple]:
        """
        Get all the monsters for this player
        """
        query = """
        SELECT * FROM monstercreated
        INNER JOIN dungeonplayer ON monstercreated.dungeonid = dungeonplayer.id
        WHERE dungeonplayer.playerid = %s
        """
        results = Database.query(query, (PlayerData.playerID,))
        return results

    @staticmethod
    def getMonsterFromMap(mapName: str) -> list[tuple]:
        """
        Get all the monster data for this player and current map
        """
        query = """
        SELECT monstercreated.positionx, monstercreated.positiony, monstercreated.id, monstercreated.health, monstercreated.speed, monstercreated.dungeonid, monster.*
        FROM monstercreated
        INNER JOIN dungeonplayer ON dungeonplayer.id = monstercreated.dungeonid
        INNER JOIN player ON dungeonplayer.playerid = player.id
        INNER JOIN world ON world.id = dungeonplayer.dungeonid
        INNER JOIN monster ON monster.id = monstercreated.monsterid
        WHERE world.name = %s AND dungeonplayer.playerid = %s
        """
        values = (mapName, PlayerData.playerID)
        results = Database.query(query, values)
        return results
