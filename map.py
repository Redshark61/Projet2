from dataclasses import dataclass
import pytmx
import pyscroll
import pygame

from player import NPC


@dataclass
class Portal:
    fromWorld: str
    toWorld: str
    originPoint: str
    destinationPoint: str


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
        # Set the current map
        self.currentMap = "assetHub/carte_hub_p2"

        # Load all the maps
        self.registerMap("assetHub/carte_hub_p2", portals=[Portal("assetHub/carte_hub_p2", "assetAir/airWorld", "toAir", "spawnPlayer"), Portal("assetHub/carte_hub_p2", "assetTerre/mapTerre", "toTerre", "spawnPlayer"), Portal(
            "assetHub/carte_hub_p2", "assetFeu/Fire_zone", "toFeu", "spawnPlayer"), Portal("assetHub/carte_hub_p2", "assetWater/WaterWorld", "toEau", "spawnPlayer"), ], entity=[NPC("Monsters/Demons/RedDemon")])
        self.registerMap("assetAir/airWorld", portals=[Portal("assetAir/airWorld", "assetHub/carte_hub_p2", "toHub", "spawnPlayer")], entity=[NPC("Monsters/Demons/RedDemon")])
        self.registerMap("assetTerre/mapTerre", portals=[Portal("assetTerre/mapTerre", "assetHub/carte_hub_p2", "toHub", "spawnPlayer")], entity=[NPC("Monsters/Demons/RedDemon")])
        self.registerMap("assetFeu/Fire_zone", portals=[Portal("assetFeu/Fire_zone", "assetHub/carte_hub_p2", "toHub", "spawnPlayer")], entity=[NPC("Monsters/Demons/RedDemon")])
        self.registerMap("assetWater/WaterWorld", portals=[Portal("assetWater/WaterWorld", "assetHub/carte_hub_p2", "toHub", "spawnPlayer")], entity=[NPC("Monsters/Demons/RedDemon")])

        self.teleportNPC("spawnBoss")

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

    def getMap(self):
        return self.maps[self.currentMap]

    def getGroup(self):
        return self.getMap().group

    def drawMap(self):
        self.getGroup().draw(self.game.screen)
        self.getGroup().center(self.game.player.rect.center)

    def updateMap(self):
        self.getGroup().update()
        self.checkCollision()
        for npc in self.getMap().npcs:
            npc.move(self.player)

    def teleportPlayer(self, destinationName):
        point = self.getObject(destinationName)
        self.player.rect.x = point.x
        self.player.rect.y = point.y
        self.player.saveLocation()

    def registerMap(self, mapName, portals, entity):
        tmxData = pytmx.util_pygame.load_pygame(f"./assets/{mapName}.tmx")
        mapData = pyscroll.data.TiledMapData(tmxData)
        mapLayer = pyscroll.orthographic.BufferedRenderer(mapData, self.screen.get_size())
        mapLayer.zoom = 2

        walls = []
        for obj in tmxData.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=20)
        group.add(self.player)

        for i in entity:
            group.add(i)

        self.maps[mapName] = Map(mapName, walls, group, tmxData, portals, entity)

    def getObject(self, name):
        return self.getMap().tmxData.get_object_by_name(name)

    def teleportNPC(self, spawnName):
        point = self.getObject(spawnName)
        for map in self.maps:
            mapData = self.maps[map]
            npcs = mapData.npcs

        for npc in npcs:
            npc.teleportSpawn(point)
