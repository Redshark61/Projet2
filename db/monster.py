from db.db import Database
from db.playerData import PlayerData


class Monster:

    @classmethod
    def addMonster(cls, dungeonID, monster):
        # Insert a new monster into the database
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
        # Update a monster in the database
        for monster in monsters:
            query = f"""
            UPDATE monstercreated
            SET positionx = {monster.rect.x}, positiony = {monster.rect.y}, health = {monster.health}
            WHERE id = {monster.index}"""
            Database.query(query)

    @staticmethod
    def getAllMonster():
        # Get the current dungeon
        query = f"""
        SELECT * FROM monstercreated
        INNER JOIN dungeonplayer ON monstercreated.dungeonid = dungeonplayer.id
        WHERE dungeonplayer.playerid = {PlayerData.playerID}
        """
        results = Database.query(query)
        return results

    @staticmethod
    def getMonsterFromMap(mapName):
        # Get the current dungeon
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

    @staticmethod
    def uploadMonster(results, monster, game):
        # Upload the monster to the game
        monster.name = results[0][1]
        monster.rect.x = results[0][2]
        monster.rect.y = results[0][3]
        monster.xp = results[0][4]
        monster.health = results[0][5]
        monster.speed = results[0][6]
        monster.alive = results[0][8]
        monster.index = results[0][9]
