from db.db import Database
from db.playerData import PlayerData


class Monster:

    @classmethod
    def addMonster(cls, dungeonID: int, monster) -> list[tuple]:
        """
        Add monster into the database
        """
        query = f"""
        INSERT INTO monstercreated
        (monsterid, positionx, positiony, health, speed, dungeonid) 
        VALUES 
        ({monster.monsterID}, '{monster.rect.x}', {monster.rect.y}, {monster.health}, {monster.speed}, {dungeonID})
        """
        Database.query(query)
        return Database.getLastID("monstercreated")

    @staticmethod
    def update(monsters):
        """
        Update the value of monster data into the database
        """
        for monster in monsters:
            query = f"""
            UPDATE monstercreated
            SET positionx = {monster.rect.x}, positiony = {monster.rect.y}, health = {monster.health}
            WHERE id = {monster.index}"""
            Database.query(query)

    @staticmethod
    def getAllMonster() -> list[tuple]:
        """
        Get all the monsters for this player
        """
        query = f"""
        SELECT * FROM monstercreated
        INNER JOIN dungeonplayer ON monstercreated.dungeonid = dungeonplayer.id
        WHERE dungeonplayer.playerid = {PlayerData.playerID}
        """
        results = Database.query(query)
        return results

    @staticmethod
    def getMonsterFromMap(mapName: str) -> list[tuple]:
        """
        Get all the monster data for this player and current map
        """
        query = f"""
        SELECT monstercreated.positionx, monstercreated.positiony, monstercreated.id, monstercreated.health, monstercreated.speed, monstercreated.dungeonid, monster.*
        FROM monstercreated
        INNER JOIN dungeonplayer ON dungeonplayer.id = monstercreated.dungeonid
        INNER JOIN player ON dungeonplayer.playerid = player.id
        INNER JOIN world ON world.id = dungeonplayer.dungeonid
        INNER JOIN monster ON monster.id = monstercreated.monsterid
        WHERE world.name = '{mapName}' AND dungeonplayer.playerid = {PlayerData.playerID}
        """
        results = Database.query(query)
        return results
