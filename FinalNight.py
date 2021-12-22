import time
import pygame
from db.db import Database
from db.playerData import PlayerData
import variables


class Night:

    periodTime = 0
    monsterStatsModified = True
    dayLength = [(None,)]
    xpModificator = 0
    healthModificator = 0
    damageModificator = 0
    timer = False
    alpha = 0

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
            variables.night = not variables.night
            print(f"Night: {variables.night}")
            cls.monsterStatsModified = False

        if variables.night and not cls.monsterStatsModified:
            for _, npc in enumerate(variables.map.getMap().npcs):
                npc.health = npc.health*cls.healthModificator
                npc.maxHealth = npc.maxHealth*cls.healthModificator
                npc.monsterDamage = npc.monsterDamage*cls.damageModificator
                npc.xp = npc.xp*cls.xpModificator
            cls.monsterStatsModified = True

        if not variables.night and not cls.monsterStatsModified:
            for _, npc in enumerate(variables.map.getMap().npcs):
                npc.maxHealth = npc.maxHealth/cls.healthModificator
                npc.health = npc.health/cls.healthModificator
                npc.monsterDamage = npc.monsterDamage/cls.damageModificator
                npc.xp = npc.xp/cls.xpModificator
            cls.monsterStatsModified = True

    @classmethod
    def drawBlueFilter(cls):
        """
        Draw blue filter on the screen
        """

        # Create a blue surface in order to apply transparency
        blueFilter = pygame.Surface((variables.screen.get_width(), variables.screen.get_width()))
        # By default the filter is transparent
        blueFilter.fill((13, 1, 138))
        blueFilter.set_alpha(cls.alpha)
        # The ratio is how much we need to add to the alpha value in the time of the period
        ratio = 150/cls.dayLength[0][0] / 3

        # If it's the night
        if variables.night:
            # Add opacity to the filter
            cls.alpha += ratio if cls.alpha < 150 else 0
            blueFilter.set_alpha(cls.alpha)
            variables.screen.blit(blueFilter, (0, 0))
        else:
            cls.alpha -= ratio if cls.alpha > 0 else 0
            blueFilter.set_alpha(cls.alpha)
            variables.screen.blit(blueFilter, (0, 0))
