from db.dungeon import Dungeon


class Monster:

    modelList = []

    def __init__(self, data):
        self.dungeonID = data[0]
        self.spritePath = data[1]
        self.position = (data[2], data[3])
        self.xp = data[4]
        self.health = data[5]
        self.speed = data[6]
        self.damage = data[7]
        self.dungeonPath = [dungeon.dungeonPath for dungeon in Dungeon.modelList if dungeon.id == self.dungeonID][0]
        Monster.modelList.append(self)
