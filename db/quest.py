from db.player import Player


class Quest:

    modelList = []

    def __init__(self, data):
        self.playerID = data[0]
        self.questPath = data[1]
        self.questName = data[2]
        self.playerName = [player.name for player in Player.modelList if player.id == self.playerID][0]
        Quest.modelList.append(self)
