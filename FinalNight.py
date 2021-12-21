import time
from db.db import Database
from db.playerData import PlayerData
import Variables


class Night:

    periodTime = 0
    monsterStatsModified = True
    dayLength = [(None,)]
    xpModificator = 0
    healthModificator = 0
    damageModificator = 0
    timer = False

    @classmethod
    def dataRecovery(cls):
        # Recover data of day's and night's modificator
        nightModificator = Database.query("SELECT * FROM nightmodificator")

        cls.xpModificator = nightModificator[0][1]
        cls.healthModificator = nightModificator[0][2]
        cls.damageModificator = nightModificator[0][3]

        # Recover data of day's and night's clock
        cls.dayLength = Database.query(f"""
        SELECT difficulty.daylength FROM difficulty
        INNER JOIN player ON player.difficultyid = difficulty.id
        WHERE player.id = {PlayerData.playerID}
        """)
        print(cls.dayLength)

    @classmethod
    def timeCheck(cls):
        """
        Launch clock of the day and modify monster's stats as it's necessary
        """

        if not cls.timer:
            actualTime = time.time()
            cls.periodTime = actualTime + cls.dayLength[0][0]
            cls.timer = True

        if time.time() > cls.periodTime:
            cls.periodTime = time.time() + cls.dayLength[0][0]
            Variables.Night = not Variables.Night
            print(f"Night: {Variables.Night}")
            cls.monsterStatsModified = False

        if Variables.Night and not cls.monsterStatsModified:
            for _, npc in enumerate(Variables.map.getMap().npcs):
                npc.health = npc.health*cls.healthModificator
                npc.maxHealth = npc.maxHealth*cls.healthModificator
                npc.monsterDamage = npc.monsterDamage*cls.damageModificator
                npc.xp = npc.xp*cls.xpModificator
            cls.monsterStatsModified = True

        if not Variables.Night and not cls.monsterStatsModified:
            for _, npc in enumerate(Variables.map.getMap().npcs):
                npc.maxHealth = npc.maxHealth/cls.healthModificator
                npc.health = npc.health/cls.healthModificator
                npc.monsterDamage = npc.monsterDamage/cls.damageModificator
                npc.xp = npc.xp/cls.xpModificator
            cls.monsterStatsModified = True
