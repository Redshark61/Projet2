import math
import random
import pygame
from db.db import Database
from db.dungeon import Dungeon
from db.playerData import PlayerData as PlayerDB
from projectile import Projectile
from musics import Music

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name: str, choice):
        super().__init__()
        # Load the asset of the required sprite
        if choice is not None:
            name = PlayerDB.getSpritePath(choice)
        self.spriteSheet = pygame.image.load(f'./assets/Characters/{name}.png')
        # The sprite sheet is divided into 3 rows of 3 images
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
        image = pygame.Surface([16, 16]).convert()
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
    def __init__(self, name, choice=None):
        super().__init__(name, choice)
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
        self.feet.midbottom = self.rect.midbottom
        self.oldPosition = self.rect.x, self.rect.y


class Player(Entity, pygame.sprite.Sprite):
    """
    Player class
    """

    def __init__(self, screen, game, name='', hasToUpload=False, choice=None):
        super().__init__(name, choice)
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
        self.playerName = name.split('/')[-1] + str(random.randint(0, 100))
        self.name = name
        self.map = 'assetHub/carte_hub_p2'
        self.projectileSound = Music()
        self.levelMusic = Music()
        self.playerDB = PlayerDB(self)
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

        pygame.draw.rect(self.screen, (100, 100, 100), [230, 0, maxWidth, height])
        pygame.draw.rect(self.screen, (0, 100, 200), [230, 0, width, height])

        # Draw the current level next to the level bar
        xpText = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 16).render(f'XP: {self.totalXP}', True, (255, 0, 0))
        self.screen.blit(xpText, (350, 2))

        # Draw the current XP next to the level bar
        levelText = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 18).render(f'LEVEL: {self.currentLevel}', True, (255, 0, 0))
        self.screen.blit(levelText, (240, 0))

    def gainXP(self, xp):
        """
        Gain XP
        """
        self.currentXP += xp
        self.totalXP += xp
        if self.currentXP >= self.maxXP:
            self.currentXP = self.currentXP - self.maxXP
            self.currentLevel += 1
            self.maxXP += 50
            self.levelMusic.playIfReady("levelUp",0)

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
        healthText = pygame.font.Font('./assets/font/Knewave-Regular.ttf', 18).render(f'Health: {round(self.health, 2)}', True, (255, 0, 0))
        self.screen.blit(healthText, (10, 0))

    def damage(self, damage):
        """
        Take damage
        """
        self.health -= damage
        self.health = max(0, self.health)
        self.drawHealthBar()

    def lauchProjectile(self):
        # create a projectile
        mousePos = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
        bomb = Projectile(self, "FireballProjectile", mousePos, self.screen)
        self.bombGroup.add(bomb)
        self.projectileSound.play("fireball",0)

    def checkCollision(self, entity):
        """
        Check if the player is colliding with an enemy
        """
        if self.rect.colliderect(entity.rect):
            self.damage(0.2)


class NPC(Entity):
    """
    Boss class
    """
    hitSound = Music()

    def __init__(self, monsterID, mapName, name, game, xp, maxHealth, speed, id=0, isDBempty=True):
        super().__init__(name)
        
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
        self.speed = speed * 0.05
        self.alive = True
        if isDBempty:
            self.index = Dungeon.addMonsters(self)

        
    def removeFromDB(self):
        query = f"""
        DELETE FROM monstercreated
        WHERE id = '{self.index}'
        """
        Database.query(query)

    def damage(self, damage):
        """
        Take damage
        """
        self.health -= damage
        self.health = max(0, self.health)
        
        self.hitSound.play("hitEnemy",0)

        if self.health <= 0:
            self.player.monsterKilled += 1
            self.player.gainXP(self.xp)
            self.kill()

    def getPosition(self):
        return self.rect.x, self.rect.y

    def move(self, player, walls):

        dx, dy = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        dist = math.hypot(dx, dy)
        try:
            dx, dy = dx / dist, dy / dist
            self.rect.y += dy * self.speed
            self.rect.x += dx * self.speed
        except ZeroDivisionError:
            self.rect.y += 0
            self.rect.x += 0

        if not self.checkCollisionWalls(walls):
            self.saveLocation()

    def teleportSpawn(self, destination):
        """
        Teleport the NPC to its spawn point
        """
        self.rect.x = destination[0]
        self.rect.y = destination[1]
        self.saveLocation()

    def hasCollided(self):
        """
        Check if the monster is colliding with a bomb
        """
        for bomb in self.player.bombGroup:

            if (self.rect.x*1.75 <= bomb.rect.x+8 <= (self.rect.x*1.75 + self.rect.width*1.75)) and (self.rect.y*1.75 <= bomb.rect.y+8 <= (self.rect.y*1.75 + self.rect.height*1.75)):
                bomb.kill()
                return True
            return False

    def checkCollisionWalls(self, walls):
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
        pygame.draw.rect(self.game.screen, (255, 0, 0), [x-centerX, y-20, maxWidth, 3])
        pygame.draw.rect(self.game.screen, (0, 255, 0), [x-centerX, y-20, width, 3])
