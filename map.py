from dataclasses import dataclass
import random
import time
import pytmx
import pyscroll
import pygame
from db.db import Database
from db.dungeon import Dungeon
from db.playerData import PlayerData
from player import NPCMonster
from quest import Quest
from db.monster import Monster as MonsterDB
from circle import Circle
import Variables as variables


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
    npcs: list[NPCMonster]


class MapManager:

    def __init__(self, game, screen):
        # Initalize the variables
        self.circle = Circle()
        self.game = game
        self.player = self.game.player
        self.screen = screen
        self.maps = {}
        self.quitButtonRect = None
        self.returnButtonRect = None
        # Set the current map
        self.currentMap = "assetHub/carte_hub_p2"

        # Get the number of monster for the current player
        self.results = MonsterDB.getAllMonster()
        # If there are no monsters yet, it means that the player is new
        self.isDBEmpty = len(self.results) == 0
        self.buttonFont = pygame.font.Font(
            "./assets/font/Knewave-Regular.ttf", 50)

        # Load the maps
        results = Database.query("SELECT * FROM world")
        # For each map
        for result in results:
            # Get the portals associated with the map
            portals = Database.query(
                f"""SELECT * FROM portals WHERE fromworld = '{result[0]}'""")
            portalsList = []

            for portal in portals:
                # Add the portal to the list
                world1 = Database.query(
                    f"""SELECT * FROM world WHERE id = {portal[1]}""")
                world2 = Database.query(
                    f"""SELECT * FROM world WHERE id = {portal[2]}""")
                portalsList.append(
                    Portal(world1[0][1], world2[0][1], portal[3], portal[4]))

            entitiesList = []
            # If the map is a dungeon, it has monsters
            if result[2]:
                # Get the monsters associated with the map
                entities = Database.query(
                    f"""SELECT * FROM monster WHERE dungeonid = '{result[0]}'""")
                for entity in entities:
                    # Add the monster to the list
                    speed = random.randint(entity[4], entity[3])
                    entitiesList.append(Monster(
                        entity[0], entity[6], entity[2], speed, entity[5], entity[1], entity[1]))

            # Register the map
            self.registerMap(result[1], portalsList, entitiesList, result[3])

        self.isDungeonFinished = False
        self.isWinScenePlaying = False
        self.timeInTimeToWait = 0

        PlayerData.setCurrentMap(self)
        self.getNumberOfDungeon()

    def getNumberOfDungeon(self):
        """
        Create all the dungeons for the current player
        """
        self.numberOfDungeon = 0
        self.listOfquest = []

        for key, value in self.maps.items():
            if "donjon" in value.name.lower():
                self.numberOfDungeon += 1
                self.listOfquest.append(Quest(key, self.screen))

    def updateDungeon(self, mapName: str):
        """
        Update the player from the database
        """
        # get the dungeon associated with the player
        results = Database.query(f"""
        SELECT * FROM dungeonplayer
        INNER JOIN world on dungeonplayer.dungeonid = world.id
        WHERE dungeonplayer.playerid = {PlayerData.playerID} and world.name = '{mapName}'
        """)
        # Add the dungeon to the database if it doesn't exist
        if len(results) == 0:
            Dungeon.addPlayer(self.player)
            Dungeon.addDungeon(mapName)

    def checkCollision(self):
        """
        Check all the collision
        """

        # Loop over all the portals
        for portal in self.getMap().portals:

            # If the portal start from the current map
            if self.currentMap == portal.fromWorld:
                # Get the coord of the portal
                point = self.getObject(portal.originPoint)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                # If the player is in the portal
                if self.player.rect.colliderect(rect):
                    copyPortal = portal
                    # Change the current map
                    self.currentMap = portal.toWorld
                    # Teleport the player to the destination
                    self.teleportPlayer(copyPortal.destinationPoint)

        # If the player touch a wall, move him back
        if self.player.feet.collidelist(self.getMap().walls) > -1:
            self.player.rect.topleft = self.player.oldPosition

        if 'feu' in self.getMap().name.lower():
            tmxData = self.getMap().tmxData
            for obj in tmxData.objects:
                if obj.type == "magma":
                    magma = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    if self.player.feet.colliderect(magma):
                        self.player.health -= 2
                        # self.respawn()

        # For each monster, check its collisions
        for npc in self.getMap().npcs:
            self.player.checkCollision(npc)

        # For every bomb, check its collisions with the walls
        for bomb in self.player.bombGroup:
            for wall in self.getMap().walls:
                if (wall.x*1.75 <= bomb.rect.x+8 <= (wall.x*1.75 + wall.width*1.75)) and (wall.y*1.75 <= bomb.rect.y+8 <= (wall.y*1.75 + wall.height*1.75)):
                    bomb.kill()

    def getMap(self) -> Map:
        """
        Get the current map
        """
        return self.maps[self.currentMap]

    def getGroup(self) -> pyscroll.PyscrollGroup:
        """
        Get the group of sprites of the current map
        """
        return self.getMap().group

    def updateMonsterInDB(self):
        """
        Update monster's data in the database
        """
        for quest in self.listOfquest:
            MonsterDB.update(self.maps[quest.originalName].npcs)

    def drawMap(self):
        """
        Draw the map
        """

        # Draw the group of the current map
        self.getGroup().draw(self.game.screen)
        self.player.map = self.currentMap

        # Draw the health bar of each monster
        for npc in self.getMap().npcs:
            npc.drawHealthBar()
        index = 1
        for quest in self.listOfquest:
            # Update every quest
            quest.updateNumberOfMonster(len(self.maps[quest.originalName].npcs))

            # If the quest is finished (no more monster)
            if len(self.maps[quest.originalName].npcs) == 0:
                # Remove the quest from the list
                self.listOfquest.remove(quest)

            # If the quest is not finished
            else:
                # re-update the quest's index in order to display it correctly when a dungeon is finished
                quest.index = index
                index += 1
                quest.tryToDrawnQuestPanel()

            # If the quest is the current map and its finished
            if self.isDungeonFinished:
                # While the current time smaller than the time we want to wait
                if time.time() < self.timeInTimeToWait:
                    if self.isWinScenePlaying:
                        # Draw the winning scene
                        # quest.winText()
                        variables.displayWinText = True
                    else:
                        self.isWinScenePlaying = True
                elif not self.isWinScenePlaying:
                    # When the time is over, we want to go back to stop displaying the scene
                    # If the time is over, we can go to the next map
                    self.isWinScenePlaying = True
                    self.timeInTimeToWait = time.time() + 5
                else:
                    variables.displayWinText = False
                    self.isDungeonFinished = False
                    self.isWinScenePlaying = False

        # draw the map in the center
        self.getGroup().center(self.game.player.rect.center)

    def updateMap(self):
        self.getGroup().update()
        self.checkCollision()

        for index, npc in enumerate(self.getMap().npcs):
            # Get the distance between the player and the monster
            distance = pygame.Vector2(self.player.rect.centerx, self.player.rect.centery).distance_to(
                (npc.rect.centerx, npc.rect.centery))
            # If the distance is smaller than the distance to attack (in px)
            if abs(distance) < 100:
                # Move the npc
                npc.move(self.player, self.getMap().walls)
            # Check if the monster has collided with a bomb
            hasMonsterCollidedWithBomb = npc.hasCollided()

            # If yes
            if hasMonsterCollidedWithBomb:
                # Deal damage to the monster, accoding to this calculation :
                damage = 6 if self.player.currentLevel == 0 else self.player.currentLevel * 10
                npc.takeDamage(damage)

            # If the monster is dead
            if npc.health <= 0:
                # delete the monster from the list
                deadMonster = self.getMap().npcs.pop(index)
                # Remove the monster from the database
                deadMonster.removeFromDB()
                # Get the number of monsters after the death of the monster
                currentNumberOfMonster = len(self.getMap().npcs)

                # If the pnumber of monster is 0, the dungeon is finished
                if currentNumberOfMonster == 0:
                    self.isDungeonFinished = True
                    # Add one level to the player
                    self.game.player.currentLevel += 1
                    # Add health to the player
                    self.game.player.maxHealth += 10
                    self.game.player.health = self.game.player.maxHealth

    def teleportPlayer(self, destinationName: str):
        """
        Teleport the player to given destination : a named point, created in Tiled
        """
        # Get the point
        point = self.getObject(destinationName)
        # Set the player's position to the point
        self.player.rect.x = point.x
        self.player.rect.y = point.y
        # Save its position
        self.player.saveLocation()
        # Make the logo appear and animate
        self.circle.rotateLogo()

    def isDead(self):
        """
        Function wich check if the player is dead
        """

        return self.player.health == 0

    def registerMap(self, mapName, portals, entityData, spawnName=""):
        """
        Add the map to the dictionary of maps, and create its monsters, monsters, walls, etc.
        """

        # Get the monster's data for the current map
        results = MonsterDB.getMonsterFromMap(mapName)
        # Load the tmx file
        tmxData = pytmx.util_pygame.load_pygame(f"./assets/{mapName}.tmx")
        mapData = pyscroll.data.TiledMapData(tmxData)
        mapLayer = pyscroll.orthographic.BufferedRenderer(
            mapData, self.screen.get_size(), clamp_camera=True)

        if 'donjon' in mapName.lower():
            # If it's a dungeon, zoom in and add the dungeon to the db
            mapLayer.zoom = 1.75
            self.updateDungeon(mapName)
        else:
            mapLayer.zoom = 2

        walls = []
        # Add the walls in the list of walls
        for obj in tmxData.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=20)
        group.add(self.player)

        entity = []
        spawnPoints = []
        # get the spawn points for every monster
        for obj in tmxData.objects:
            if obj.type == spawnName and spawnName is not None:
                spawnPoints.append((obj.x, obj.y))

        # For every spawn point
        for i, spawnPoint in enumerate(spawnPoints):
            # If the db is empty
            if self.isDBEmpty:
                # Add the monster into it
                randomMonster = random.choice(entityData)
                monster = NPCMonster(randomMonster.id, mapName, randomMonster.name,
                                     self.game, randomMonster.xp, randomMonster.health, randomMonster.speed, randomMonster.damage)
                entity.append(monster)
                group.add(monster)
            else:
                # If the db is not empty, and the list isn't empty : get the monster from the db
                if len(results) > 0:
                    try:
                        # Create the monster and update its value with the data from the db
                        if results[i][7]:
                            monster = NPCMonster(results[i][0], mapName, results[i][14], self.game,
                                                 results[i][10], results[i][9], results[i][5], results[i][13], results[i][3], self.isDBEmpty)
                            monster.rect.x = results[i][1]
                            monster.rect.y = results[i][2]
                            monster.alive = True
                            entity.append(monster)
                            group.add(monster)
                    # There is IndexError when there is no more monster in the db
                    except IndexError:
                        break

        # Add the map into the dictionary
        self.maps[mapName] = Map(
            mapName, walls, group, tmxData, portals, entity)

        # teleport monsters to their spawn point
        for monster, spawnPoint in zip(entity, spawnPoints):
            self.teleportNPC(spawnPoint, monster)

    def getObject(self, name: str, mapData=None) -> pytmx.TiledObject:
        """
        get an object from a tmx map using its name
        """
        if mapData is None:
            return self.getMap().tmxData.get_object_by_name(name)
        return mapData.tmxData.get_object_by_name(name)

    @staticmethod
    def teleportNPC(point, npc: NPCMonster):
        """
        Teleport the monster to a given point
        """
        npc.teleportSpawn(point)
