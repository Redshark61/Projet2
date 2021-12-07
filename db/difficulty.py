class Difficulty:

    modelList = []

    def __init__(self, data):
        self.ID = data[0]
        self.name = data[1]
        self.coef = data[2]
        Difficulty.modelList.append(self)

    def __str__(self) -> str:
        return f"ID: {self.ID}, name: {self.name}, coef: {self.coef}"
