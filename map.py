import pytmx
import pyscroll


class Map:

    def __init__(self, game, entity: list):
        self.game = game
        # Load the map
        self.tmxData = pytmx.load_pygame("./assets/carte_hub_p2.tmx")
        mapData = pyscroll.data.TiledMapData(self.tmxData)
        mapLayer = pyscroll.BufferedRenderer(mapData, game.screen.get_size())
        mapLayer.zoom = 2

        self.group = pyscroll.PyscrollGroup(map_layer=mapLayer, default_layer=18)
        for i in entity:
            self.group.add(i)

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
