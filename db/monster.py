from db.db import Database


class Monster:

    @classmethod
    def addMonster(cls, dungeonID, monster, index):
        # Insert a new monster into the database
        query = f"""
        INSERT INTO monster 
        (dungeonid, spritepath, positionx, positiony, health, speed, xp, id) 
        VALUES 
        ({dungeonID}, '{monster.name}', {monster.rect.x}, {monster.rect.y}, {monster.health}, {monster.speed}, {monster.xp}, {index})"""

        Database.query(query)

    @staticmethod
    def update(monsters):
        # Update a monster in the database
        for monster in monsters:
            query = f"""
            UPDATE monster 
            SET positionx = {monster.rect.x}, positiony = {monster.rect.y}, health = {monster.health}, updated = true
            WHERE id = {monster.index}"""
            Database.query(query)
