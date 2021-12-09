from db.db import Database
from db.playerData import PlayerData


class Monster:

    @classmethod
    def addMonster(cls, dungeonID, monster):
        # Insert a new monster into the database
        query = f"""
        INSERT INTO monster 
        (dungeonid, spritepath, positionx, positiony, health, speed, xp) 
        VALUES 
        ({dungeonID}, '{monster.name}', {monster.rect.x}, {monster.rect.y}, {monster.health}, {monster.speed}, {monster.xp})
        """
        Database.query(query)

        # Get the id of the last monster inserted
        query = """
        SELECT id FROM monster
        ORDER BY id DESC
        LIMIT 1
        """
        id = Database.query(query)[0][0]

        return id

    @staticmethod
    def update(monsters):
        # Update a monster in the database
        for monster in monsters:
            query = f"""
            UPDATE monster 
            SET positionx = {monster.rect.x}, positiony = {monster.rect.y}, health = {monster.health}
            WHERE id = {monster.index}"""
            Database.query(query)

    @staticmethod
    def getAllMonster():
        # Get the current dungeon
        query = """
        SELECT * FROM monster
        INNER JOIN dungeon ON monster.dungeonid = dungeon.id
        INNER JOIN player ON dungeon.playerid = player.id
        """
        results = Database.query(query)
        return results

    @staticmethod
    def getMonsterFromMap(mapName):
        # Get the current dungeon
        query = f"""
        SELECT monster.dungeonid, monster.spritepath, monster.positionx, monster.positiony, monster.xp, monster.health, monster.speed, monster.damage, monster.alive, monster.id
        FROM monster
        INNER JOIN dungeon ON monster.dungeonid = dungeon.id
        INNER JOIN player ON dungeon.playerid = player.id
        WHERE dungeon.dungeonpath = '{mapName}' AND dungeon.playerid = {PlayerData.playerID}
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
