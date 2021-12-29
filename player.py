import math
import pygame
from db.db import Database
from db.dungeon import Dungeon
from db.playerData import PlayerData as PlayerDB
from projectile import Projectile
from musics import Music


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name: str, choice: int):
        super().__init__()
        # Load the asset of the required sprite
        if choice is not None:
            name = PlayerDB.getSpritePath(choice)

        # Load the sprite sheet
        self.spriteSheet = pygame.image.load(f'./assets/Characters/{name}.png')
        self.animationIndex = 0
        # Get differents images of the player when he moves
        self.images = {
            'down': self.getImages(0),
            'up': self.getImages(1*16),
            'right': self.getImages(2*16),
            'left': self.getImages(3*16)
        }
        self.image = ""
        self.clock = 0
        self.speed = 2

    def getImage(self, x: int, y: int) -> pygame.Surface:
        """
        Return a single image from the sprite sheet
        """
        # Create a new surface for the player
        image = pygame.Surface([16, 16]).convert()

        # Get the image from the sprite sheet at the given position
        image.blit(self.spriteSheet, (0, 0), (x, y, 16, 16))
        image.set_colorkey([0, 0, 0])
        return image

    def getImages(self, y: int) -> list[pygame.Surface]:
        """
        Create a list of all the images of the player depending on the direction (each direction is a different row)
        """
        images = []
        for i in range(0, 5):
            x = i * 16
            image = self.getImage(x, y)
            images.append(image)

        return images

    def changeAnimation(self, name: str):
        """
        return the current state of the animation
        """
        # Get the current image of the animation
        self.image = self.images[name][self.animationIndex]
        self.image.set_colorkey([0, 0, 0])
        # Add a clock not to animate at 60fps
        self.clock += self.speed * 8

        if self.clock >= 100:
            # When needed, the animation index is increased
            self.animationIndex += 1
            if self.animationIndex >= len(self.images[name]):
                self.animationIndex = 0
            self.clock = 0


class Entity(AnimateSprite):

    def __init__(self, name: str, choice=None):
        super().__init__(name, choice)
        # Get the first image of the animation
        self.image = self.getImage(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.velocity = 3
        self.oldPosition = self.rect.x, self.rect.y
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 6)

    def update(self):
        """
        Update the position of the player on the map
        """
        self.rect.topleft = self.rect.x, self.rect.y
        self.feet.midbottom = self.rect.midbottom

    def moveUp(self):
        self.rect.y -= self.velocity
        self.changeAnimation('up')

    def moveDown(self):
        self.rect.y += self.velocity
        self.changeAnimation('down')

    def moveLeft(self):
        self.rect.x -= self.velocity
        self.changeAnimation('left')

    def moveRight(self):
        self.rect.x += self.velocity
        self.changeAnimation('right')

    def saveLocation(self):
        """
        Save the current position of the player
        """
        self.feet.midbottom = self.rect.midbottom
        self.oldPosition = self.rect.x, self.rect.y


class Player(Entity, pygame.sprite.Sprite):
    """
    Player class
    """

    def __init__(self, screen: pygame.Surface, game, path: str = '', name='', hasToUpload: bool = False, choice: bool = None, difficulty: int = None):
        super().__init__(path, choice)
        self.difficulty = difficulty
        self.game = game
        self.bombGroup = pygame.sprite.Group()
        self.screen = screen
        self.maxHealth = 100
        self.bomb = ''
        self.health = self.maxHealth
        self.monsterKilled = 0
        self.maxXP = 100
        self.currentXP = 0
        self.currentLevel = 0
        self.totalXP = 0
        # The player name is the name of the file + random number
        self.playerName = name
        self.name = path
        self.map = 'assetHub/carte_hub_p2'
        # Set up the sounds
        self.projectileSound = Music()
        self.levelMusic = Music()
        # Set up the player for the database
        self.playerDB = PlayerDB(self)

        # If the player has not to upload, add it to the database
        if not hasToUpload:
            self.playerDB.addToList()
        else:
            self.playerDB.upload(self, choice)

    def drawLevelBar(self):
        """
        Draw the level bar
        """
        maxWidth = 200
        width = self.currentXP / self.maxXP * 200
        height = 30

        pygame.draw.rect(self.screen, (100, 100, 100),
                         [230, 0, maxWidth, height])
        pygame.draw.rect(self.screen, (0, 100, 200), [230, 0, width, height])

        # Draw the current level next to the level bar
        xpText = pygame.font.Font('./assets/font/Knewave-Regular.ttf',
                                  16).render(f'XP: {self.totalXP}', True, (255, 0, 0))
        self.screen.blit(xpText, (350, 2))

        # Draw the current XP next to the level bar
        levelText = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 18).render(
            f'LEVEL: {self.currentLevel}', True, (255, 0, 0))
        self.screen.blit(levelText, (240, 0))

    def gainXP(self, xp: int):
        """
        Gain XP
        """
        self.currentXP += int(xp)
        self.totalXP += int(xp)
        self.health = self.health + int(xp) / 5 if (self.health + int(xp) /
                                                    5) < self.maxHealth else self.maxHealth

        # If the player has enough XP, level up
        if self.currentXP >= self.maxXP:
            self.currentXP = self.currentXP - self.maxXP
            self.currentLevel += 1
            self.maxXP += 50
            self.levelMusic.playIfReady("levelUp", 0)

    def drawHealthBar(self):
        """
        Draw the health bar
        """
        maxWidth = 200
        height = 30
        width = self.health / self.maxHealth * 200
        pygame.draw.rect(self.screen, (255, 0, 0), [0, 0, maxWidth, height])
        pygame.draw.rect(self.screen, (0, 255, 0), [0, 0, width, height])

        # Write the current health on the screen under the health bar
        healthText = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 18).render(
            f'Health: {round(self.health, 2)}', True, (255, 0, 0))
        self.screen.blit(healthText, (10, 0))

    def damage(self, damage: int):
        """
        Take damage
        """
        self.health -= damage + (self.currentLevel*0.75)
        self.health = max(0, self.health)
        self.drawHealthBar()

    def lauchProjectile(self):
        """
        Launch the projectile
        """

        # Get the mouse's position
        mousePos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]

        # Create a new projectile
        bomb = Projectile(self, "FireballProjectile", mousePos, self.screen)
        self.bombGroup.add(bomb)
        self.projectileSound.play("fireball", 0)

    def checkCollision(self, entity: pygame.Rect):
        """
        Check if the player is colliding with an enemy
        """
        if self.rect.colliderect(entity.rect):
            self.damage(entity.monsterDamage/10)


class NPCMonster(Entity):
    """
    Boss class
    """
    hitSound = Music()

    def __init__(self, monsterID: int, mapName: str, name: str, game, xp: int, maxHealth: int, speed: int, monsterDamage: int, id: int = 0, isDBempty: bool = True):
        super().__init__(name)
        # Set up the properties of the monster from the database
        self.name = name
        self.index = id
        self.monsterID = monsterID
        self.xp = xp
        self.mapName = mapName
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.direction = "right"
        self.game = game
        self.monster = pygame.sprite.GroupSingle()
        self.player = self.game.player
        self.speed = speed
        self.monsterDamage = monsterDamage
        self.alive = True
        # If there are no monster for the given player, add it to the database
        if isDBempty:
            self.index = Dungeon.addMonsters(self)

    def removeFromDB(self):
        """
        Remove the monster from the database
        """

        query = f"""
        DELETE FROM monstercreated
        WHERE id = '{self.index}'
        """
        Database.query(query)

    def takeDamage(self, damage: int):
        """
        Take damage
        """
        # Decrease the health
        self.health -= damage
        self.health = max(0, self.health)

        self.hitSound.play("hitEnemy", 0)

        if self.health <= 0:
            # when the player is dead, kill the monster and add the xp to the player
            self.player.monsterKilled += 1
            self.player.gainXP(self.xp)
            self.kill()

    def move(self, player: Player, walls: list[pygame.Rect]):
        """
        make the monster move towards the player, and stop it when it collides with a wall
        """

        start = pygame.Vector2(self.rect.center)
        end = pygame.Vector2(player.rect.center)
        try:
            direction = (end - start).normalize() * (self.speed / 30+1)
        except ValueError:
            direction = pygame.Vector2(0, 0)
        self.rect.x += direction.x
        self.rect.y += direction.y

        if not self.checkCollisionWalls(walls):
            self.saveLocation()

    def teleportSpawn(self, destination: list[int, int]):
        """
        Teleport the NPCMonster to its spawn point
        """
        self.rect.x = destination[0]
        self.rect.y = destination[1]
        self.saveLocation()

    def hasCollided(self) -> bool:
        """
        Check if the monster is colliding with a bomb
        """
        for bomb in self.player.bombGroup:

            if (self.rect.x*1.75 <= bomb.rect.x+8 <= (self.rect.x*1.75 + self.rect.width*1.75)) and (self.rect.y*1.75 <= bomb.rect.y+8 <= (self.rect.y*1.75 + self.rect.height*1.75)):
                bomb.kill()
                return True
            return False

    def checkCollisionWalls(self, walls: list[pygame.Rect]) -> bool:
        """
        Check if the monster is colliding with a wall
        """
        if self.rect.collidelist(walls) > -1:
            self.rect.topleft = self.oldPosition
            return True
        return False

    def drawHealthBar(self):
        """
        Draw the health bar
        """
        maxWidth = 100
        width = self.health / self.maxHealth * 100
        x, y = self.rect.x*1.75+8, self.rect.y*1.75+8
        # Get the center of the bar in order to place it above the monster
        centerX = maxWidth//2 - 8
        pygame.draw.rect(self.game.screen, (255, 0, 0),
                         [x-centerX, y-20, maxWidth, 3])
        pygame.draw.rect(self.game.screen, (0, 255, 0),
                         [x-centerX, y-20, width, 3])
