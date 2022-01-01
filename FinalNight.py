import time
import pygame
from db.db import Database
from db.playerData import PlayerData
import Variables as variables


class Night:

    # Const status stats
    UNINIT = 0
    DAY = 1
    NIGHT = 2
    # Locals
    status=UNINIT
    periodTime = 0
    monsterStatsModified = True
    dayLength = None
    xpModificator = 0.0
    healthModificator = 0.0
    damageModificator = 0.0
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
        """)[0][0]

    @classmethod
    def timeCheck(cls):
        """
        Launch clock of the day and modify monster's stats as it's necessary
        """
        if cls.status == cls.UNINIT:
        # Initilize timer at first time
            cls.periodTime = time.time() + cls.dayLength
            cls.status = cls.DAY

        elif  time.time() > cls.periodTime:
            cls.periodTime = time.time() + cls.dayLength
            
            if cls.status==cls.DAY:
                cls.status = cls.NIGHT
            else:
                cls.status = cls.DAY
            cls.updateNPC()


    @classmethod
    def updateNPC(cls):        
        for npc in variables.map.getMap().npcs:
            if cls.status == cls.DAY:
                npc.health = npc.health/cls.healthModificator
                npc.maxHealth = npc.maxHealth/cls.healthModificator
                npc.monsterDamage = npc.monsterDamage/cls.damageModificator
                npc.xp = npc.xp/cls.xpModificator
            
            elif cls.status == cls.NIGHT:
                npc.health = npc.health*cls.healthModificator
                npc.maxHealth = npc.maxHealth*cls.healthModificator
                npc.monsterDamage = npc.monsterDamage*cls.damageModificator
                npc.xp = npc.xp*cls.xpModificator

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
        ratio = 150/cls.dayLength / 3

        # If it's the night
        if cls.status==cls.NIGHT:
            # Add opacity to the filter
            cls.alpha += ratio if cls.alpha < 150 else 0
            blueFilter.set_alpha(cls.alpha)
            variables.screen.blit(blueFilter, (0, 0))
        else:
            cls.alpha -= ratio if cls.alpha > 0 else 0
            blueFilter.set_alpha(cls.alpha)
            variables.screen.blit(blueFilter, (0, 0))

