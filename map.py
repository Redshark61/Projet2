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
from musics import Music


@dataclass
class Portal:
    fromWorld: str
    toWorld: str
    originPoint: str
    destinationPoint: str


@dataclass
class Monster:
    id: int
    name: str
    xp: int
    speed: int
    damage: int
    maxHealth: int = 100
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
        self.circle = Circle()
        self.playMusic = Music()
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
        self.buttonFont = pygame.font.Font("./assets/font/Knewave-Regular.ttf", 50)


        results = Database.query("SELECT * FROM world")
        for result in results:
            portals = Database.query(f"""SELECT * FROM portals WHERE fromworld = '{result[0]}'""")
            portalsList = []

            for portal in portals:
                world1 = Database.query(f"""SELECT * FROM world WHERE id = {portal[1]}""")
                world2 = Database.query(f"""SELECT * FROM world WHERE id = {portal[2]}""")
                portalsList.append(Portal(world1[0][1], world2[0][1], portal[3], portal[4]))

            entitiesList = []
            if result[2]:
                entities = Database.query(f"""SELECT * FROM monster WHERE dungeonid = '{result[0]}'""")
                for entity in entities:
                    speed = random.randint(entity[4], entity[3])
                    entitiesList.append(Monster(entity[0], entity[6], entity[2], speed, entity[5], entity[1], entity[1]))

            self.registerMap(result[1], portalsList, entitiesList, result[3])
        self.isDungeonFinished = False
        self.isWinScenePlaying = False
        self.timeInTimeToWait = 0

        PlayerData.setCurrentMap(self)
        self.getNumberOfDungeon()

    def getNumberOfDungeon(self):
        self.numberOfDungeon = 0
        self.listOfquest = []

        for key, value in self.maps.items():
            if "donjon" in value.name.lower():
                self.numberOfDungeon += 1
                self.listOfquest.append(Quest(key, self.screen))

    def updateDungeon(self, mapName):
        """
        Update the player from the database
        """
        results = Database.query(f"""
        SELECT * FROM dungeonplayer
        INNER JOIN world on dungeonplayer.dungeonid = world.id
        WHERE dungeonplayer.playerid = {PlayerData.playerID} and world.name = '{mapName}'
        """)
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

        self.circle.rotateLogo()

        if "donjon" in self.currentMap:
            self.playMusic.play("dungeon", -1)
        else:
            self.playMusic.play("outdoor", -1)
            
        self.playMusic.setVolume(0.05)
    def respawn(self):

        if self.player.health == 0:
            #             self.currentMap = "assetHub/carte_hub_p2"
            #             self.teleportPlayer("spawnPlayer")
            #             self.player.health = self.player.maxHealth

            background = pygame.image.load('assets/Background Game Over.png')
            background2 = pygame.Surface(self.screen.get_size())
            background2.fill((0, 0, 0))
            banner = pygame.image.load('assets/Banner Game Over.png')
            quitButton = self.buttonFont.render("Quitter", True, (255, 255, 255))
            returnButton = self.buttonFont.render("Retour", True, (255, 255, 255))

            self.screen.blit(background2, (0, 0))
            self.screen.blit(background, (30, 0))
            self.screen.blit(banner, (280, 50))
            self.screen.blit(quitButton, (800, 600))
            self.quitButtonRect = quitButton.get_rect()
            self.quitButtonRect.x, self.quitButtonRect.y = 800, 600
            self.screen.blit(returnButton, (100, 600))
            self.returnButtonRect = returnButton.get_rect()
            self.returnButtonRect.x, self.returnButtonRect.y = 100, 600

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
            if obj.type == spawnName and spawnName is not None:
                spawnPoints.append((obj.x, obj.y))

        for i, spawnPoint in enumerate(spawnPoints):
            if self.isDBEmpty:
                randomMonster = random.choice(entityData)
                monster = NPC(randomMonster.id, mapName, randomMonster.name, self.game, randomMonster.xp, randomMonster.health, randomMonster.speed)
                entity.append(monster)
                group.add(monster)
            else:
                if len(results) > 0:
                    try:
                        if results[i][8]:
                            monster = NPC(results[i][6], mapName, results[i][12], self.game, results[i][8], results[i][7], results[i][9], results[i][2], self.isDBEmpty)
                            monster.rect.x = results[i][0]
                            monster.rect.y = results[i][1]
                            monster.alive = True
                            entity.append(monster)
                            group.add(monster)
                    except IndexError:
                        break

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
