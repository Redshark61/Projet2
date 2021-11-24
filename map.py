from dataclasses import dataclass
import pytmx
import pyscroll
import pygame


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


class MapManager:

    def __init__(self, game, entity: list):
        self.game = game
        self.maps = {}
        # Load the map
        self.currentMap = "assetHub/carte_hub_p2"
        self.tmxData = pytmx.load_pygame("./assets/assetHub/carte_hub_p2.tmx")
        mapData = pyscroll.data.TiledMapData(self.tmxData)
        mapLayer = pyscroll.BufferedRenderer(mapData, game.screen.get_size())
        mapLayer.zoom = 2

        self.group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=18)
        for i in entity:
            self.group.add(i)

    def checkCollision(self):
        if self.currentMap == Portal.fromWorld:
            pass

    def drawMap(self):
        self.group.draw(self.game.screen)
        self.group.center(self.game.player.rect.center)

    def updateMap(self):
        self.group.update()

    def teleportPlayer(self, objectName, entity):
        # Get the tmx obejct with the name "playerSpawn"
        spawn = self.tmxData.get_object_by_name(objectName)
        # Set the player's position to the spawn point
        entity.rect.x = spawn.x
        entity.rect.y = spawn.y

    def registerMap(self, mapName, portals):
        tmxData = pytmx.util_pygame.load_pygame(f"./assets/{mapName}.tmx")
        mapData = pyscroll.data.TiledMapData(tmxData)
        mapLayer = pyscroll.orthographic.BufferedRenderer(mapData, self.screen.get_size())
        mapLayer.zoom = 2

        walls = []
        for object in self.tmxData.objects:
            if object.name == "collision":
                walls.append(pygame.Rect(object.x, object.y, object.width, object.height))

        group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=5)
        group.add(self.player)

        self.maps[mapName] = Map(mapName, walls, group, self.tmxData, portals)
