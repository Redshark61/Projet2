from dataclasses import dataclass
import random
import time
import pytmx
import pyscroll
import pygame
from db.db import Database
from db.dungeon import Dungeon
from db.playerData import PlayerData
from player import NPC
from quest import Quest
from db.monster import Monster as MonsterDB
from circle import Circle


@dataclass
class Portal:
    fromWorld: str
    toWorld: str
    originPoint: str
    destinationPoint: str


@dataclass
class Monster:
    name: str
    xp: int
    speed: int
    health: int = 100


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmxData: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]


class MapManager:

    def __init__(self, game, screen):
        # Initalize the variables
        self.game = game
        self.player = self.game.player
        self.screen = screen
        self.maps = {}
        self.quitButtonRect = None
        self.returnButtonRect = None
        # Set the current map
        self.currentMap = "assetHub/carte_hub_p2"
        self.results = MonsterDB.getAllMonster()
        self.isDBEmpty = len(self.results) == 0
        self.registerMap("assetHub/carte_hub_p2",
                         portals=[
                             Portal("assetHub/carte_hub_p2", "assetAir/airWorld", "toAir", "spawnPlayer"),
                             Portal("assetHub/carte_hub_p2", "assetTerre/mapTerre", "toTerre", "spawnPlayer"),
                             Portal("assetHub/carte_hub_p2", "assetFeu/Fire_zone2", "toFeu", "spawnPlayer"),
                             Portal("assetHub/carte_hub_p2", "assetWater/WaterWorld", "toEau", "spawnPlayer"),
                             Portal("assetHub/carte_hub_p2", "assetHub/donjonHub/carteDonjonHub", "toDonjonHub", "spawnPlayer"),
                         ], entityData=[])

        self.registerMap("assetAir/airWorld",
                         portals=[
                             Portal("assetAir/airWorld", "assetHub/carte_hub_p2", "toHub", "fromAir"),
                             Portal("assetAir/airWorld", "assetAir/donjon/donjon", "toAirDonjon", "spawnPlayer"),
                         ],
                         entityData=[])

        self.registerMap("assetTerre/mapTerre",
                         portals=[
                             Portal("assetTerre/mapTerre", "assetHub/carte_hub_p2", "toHub", "fromTerre"),
                             Portal("assetTerre/mapTerre", "assetTerre/donjon/donjon", "toTerreDonjon", "spawnPlayer"),
                         ],
                         entityData=[])
        self.registerMap("assetFeu/Fire_zone2", portals=[Portal("assetFeu/Fire_zone2", "assetHub/carte_hub_p2", "toHub", "fromFeu")], entityData=[])
        self.registerMap("assetWater/WaterWorld",
                         portals=[
                             Portal("assetWater/WaterWorld", "assetHub/carte_hub_p2", "toHub", "fromEau"),
                             Portal("assetWater/WaterWorld", "assetWater/donjon/Donjon eau", "toWaterDonjon", "spawnPlayer"),
                         ],
                         entityData=[])

        self.registerMap("assetTerre/donjon/donjon",
                         portals=[Portal("assetTerre/donjon/donjon", "assetTerre/mapTerre", "toTerre", "spawnToDonjon")],
                         entityData=[
                             Monster("Monsters/Demons/PurpleDemon", xp=30, speed=(50, 60)),
                             Monster("Monsters/Orcs/KamikazeGoblin", xp=50, health=200, speed=(20, 30)),
                         ],
                         spawnName="TerreSpawnMonster")

        self.registerMap("assetAir/donjon/donjon",
                         portals=[Portal("assetAir/donjon/donjon", "assetAir/airWorld", "toAir", "spawnPlayer")],
                         entityData=[
                             Monster("Monsters/Demons/RedDemon", xp=30, speed=(50, 60)),
                             Monster("Monsters/Orcs/Orc", xp=50, health=200, speed=(20, 30)),
                         ],
                         spawnName="AirSpawnMonster")

        self.registerMap("assetHub/donjonHub/carteDonjonHub",
                         portals=[Portal("assetHub/donjonHub/carteDonjonHub", "assetHub/carte_hub_p2", "toHub", "spawnPlayer")],
                         entityData=[
                             Monster("Monsters/Demons/RedDemon", xp=30, speed=(50, 60)),
                             Monster("Monsters/Orcs/Orc", xp=50, health=200, speed=(20, 30)),
                         ],
                         spawnName="hubSpawnMonster")

        self.registerMap("assetWater/donjon/Donjon eau",
                         portals=[Portal("assetWater/donjon/Donjon eau", "assetWater/WaterWorld", "toWater", "spawnPlayer")],
                         entityData=[
                             Monster("Monsters/Pirates/PirateCaptain", xp=70, speed=(50, 60)),
                             Monster("Monsters/Pirates/PirateGunner", xp=50, health=200, speed=(20, 30)),
                             Monster("Monsters/Pirates/PirateGrunt", xp=30, speed=(15, 25))
                         ],
                         spawnName="waterSpawnMonster")

        self.isDungeonFinished = False
        self.isWinScenePlaying = False
        self.timeInTimeToWait = 0
        # NPC.uploadFromDB(self.maps)
        PlayerData.setCurrentMap(self)
        self.getNumberOfDungeon()

    def getNumberOfDungeon(self):
        self.numberOfDungeon = 0
        self.listOfquest = []

        for key, value in self.maps.items():
            if "donjon" in value.name:
                self.numberOfDungeon += 1
                self.listOfquest.append(Quest(key, self.screen))

    def updateDungeon(self, mapName):
        """
        Update the player from the database
        """
        results = Database.query(f"SELECT * FROM dungeon WHERE playerid = '{PlayerData.playerID}' and dungeon.dungeonpath = '{mapName}'")
        if len(results) == 0:
            Dungeon.addPlayer(self.player)
            Dungeon.addDungeon(mapName)

    def checkCollision(self):
        # Loop over all the portals
        for portal in self.getMap().portals:
            # If the portal start from the current map
            if self.currentMap == portal.fromWorld:
                point = self.getObject(portal.originPoint)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.rect.colliderect(rect):
                    copyPortal = portal
                    self.currentMap = portal.toWorld
                    self.teleportPlayer(copyPortal.destinationPoint)

        if self.player.feet.collidelist(self.getMap().walls) > -1:
            self.player.rect.topleft = self.player.oldPosition

        for npc in self.getMap().npcs:
            self.player.checkCollision(npc)

        for bomb in self.player.bombGroup:
            for wall in self.getMap().walls:
                if (wall.x*1.75 <= bomb.rect.x+8 <= (wall.x*1.75 + wall.width*1.75)) and (wall.y*1.75 <= bomb.rect.y+8 <= (wall.y*1.75 + wall.height*1.75)):
                    bomb.kill()

    def getMap(self):
        return self.maps[self.currentMap]

    def getGroup(self):
        return self.getMap().group

    def updateMonsterInDB(self):
        for quest in self.listOfquest:
            MonsterDB.update(self.maps[quest.originalName].npcs)

    def drawMap(self):
        self.getGroup().draw(self.game.screen)
        self.player.map = self.currentMap
        for npc in self.getMap().npcs:
            npc.drawHealthBar()

        for quest in self.listOfquest:
            quest.updateNumberOfMonster(len(self.maps[quest.originalName].npcs))
            quest.tryToDrawnQuestPanel()

            if quest.originalName == self.currentMap and self.isDungeonFinished:
                timeToWait = 5
                if self.isWinScenePlaying:
                    if time.time() < self.timeInTimeToWait:
                        quest.winText()
                    else:
                        self.isDungeonFinished = False
                        self.isWinScenePlaying = False
                else:
                    self.isWinScenePlaying = True
                    self.timeInTimeToWait = time.time() + timeToWait

        self.getGroup().center(self.game.player.rect.center)

    def updateMap(self):
        self.getGroup().update()
        self.checkCollision()

        for index, npc in enumerate(self.getMap().npcs):
            npc.drawHealthBar()
            npc.move(self.player, self.getMap().walls)
            bomb = npc.hasCollided()
            if bomb:
                damage = 6 if self.player.currentLevel == 0 else self.player.currentLevel * 10
                npc.damage(damage)
            if npc.health <= 0:
                previousNumberOfMonster = len(self.getMap().npcs)
                deadMonster = self.getMap().npcs.pop(index)
                deadMonster.removeFromDB()
                currentNumberOfMonster = len(self.getMap().npcs)

                if previousNumberOfMonster == 1 and currentNumberOfMonster == 0:
                    self.isDungeonFinished = True
                    previousNumberOfMonster = 0

            if self.getMap().npcs == []:
                self.game.player.currentLevel += 1
                self.game.player.maxHealth += 10
                self.game.player.health = self.game.player.maxHealth

            # Make the monster of the current map move

    def teleportPlayer(self, destinationName):
        
        point = self.getObject(destinationName)
        self.player.rect.x = point.x
        self.player.rect.y = point.y
        self.player.saveLocation()

        circle = Circle()
        circle.rotateLogo()

    def respawn(self):

        if self.player.health == 0:
#             self.currentMap = "assetHub/carte_hub_p2"
#             self.teleportPlayer("spawnPlayer")
#             self.player.health = self.player.maxHealth

            background = pygame.image.load('assets/Background Game Over.png')
            background2 = pygame.Surface(self.screen.get_size())
            background2.fill((0, 0, 0))
            banner = pygame.image.load('assets/Banner Game Over.png')
            quitButton = pygame.image.load('assets/Quit Button.png')
            returnButton = pygame.image.load('assets/RetourMenu.png')

            self.screen.blit(background2, (0, 0))
            self.screen.blit(background, (30, 0))
            self.screen.blit(banner, (280,50))
            self.screen.blit(quitButton, (750,600))
            self.quitButtonRect = quitButton.get_rect()
            self.quitButtonRect.x, self.quitButtonRect.y = 750, 600
            self.screen.blit(returnButton, (30,600))
            self.returnButtonRect = returnButton.get_rect()
            self.returnButtonRect.x, self.returnButtonRect.y = 30, 600


            pygame.display.flip()

    def registerMap(self, mapName, portals, entityData, spawnName=""):
        results = MonsterDB.getMonsterFromMap(mapName)
        tmxData = pytmx.util_pygame.load_pygame(f"./assets/{mapName}.tmx")
        mapData = pyscroll.data.TiledMapData(tmxData)
        mapLayer = pyscroll.orthographic.BufferedRenderer(mapData, self.screen.get_size(), clamp_camera=True)

        if 'donjon' in mapName.lower():
            mapLayer.zoom = 1.75
            self.updateDungeon(mapName)
        else:
            mapLayer.zoom = 2

        walls = []
        for obj in tmxData.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=20)
        group.add(self.player)

        entity = []
        spawnPoints = []
        for obj in tmxData.objects:
            if obj.type == spawnName:
                spawnPoints.append((obj.x, obj.y))

        for i, spawnPoint in enumerate(spawnPoints):
            if self.isDBEmpty:
                randomMonster = random.choice(entityData)
                entityName = randomMonster.name
                entityXP = randomMonster.xp
                entityHealth = randomMonster.health
                entitySpeed = random.randint(randomMonster.speed[0], randomMonster.speed[1]) / 20
                monster = NPC(mapName, entityName, self.game, entityXP, entityHealth, entitySpeed)
                entity.append(monster)
                group.add(monster)
            else:
                if results[i][8]:
                    monster = NPC(mapName, results[i][1], self.game, results[i][4], results[i][5], results[i][6], self.isDBEmpty)
                    monster.rect.x = results[i][2]
                    monster.rect.y = results[i][3]
                    monster.alive = results[i][8]
                    monster.index = results[i][9]
                    entity.append(monster)
                    group.add(monster)

        self.maps[mapName] = Map(mapName, walls, group, tmxData, portals, entity)

        for monster, spawnPoint in zip(entity, spawnPoints):
            self.teleportNPC(spawnPoint, monster)

    def getObject(self, name, mapData=None):
        if mapData is None:
            return self.getMap().tmxData.get_object_by_name(name)
        return mapData.tmxData.get_object_by_name(name)

    @staticmethod
    def teleportNPC(point, npc):
        npc.teleportSpawn(point)
