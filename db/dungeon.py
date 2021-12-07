class Dungeon:

    modelList = []

    def __init__(self, data):
        self.ID = data[0]
        self.dungeonPath = data[1]
        Dungeon.modelList.append(self)
