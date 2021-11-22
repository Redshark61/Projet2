import pygame

from projectile import Projectile


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name: str, sideLength):
        super().__init__()
        self.sideLength = sideLength
        # Load the asset of the required sprite
        self.spriteSheet = pygame.image.load(f'./assets/Characters/{name}.png')
        # The sprite sheet is divided into 3 rows of 3 images
        self.animationIndex = 0

        # Get differents images of the player when he moves
        self.images = {
            'down': self.getImages(0),
            'up': self.getImages(1*sideLength),
            'right': self.getImages(2*sideLength),
            'left': self.getImages(3*sideLength)
        }
        self.image = ""
        self.clock = 0
        self.speed = 2

    def getImage(self, x: int, y: int) -> pygame.Surface:
        """
        Return a single image from the sprite sheet
        """
        image = pygame.Surface([self.sideLength, self.sideLength]).convert()
        image.blit(self.spriteSheet, (0, 0), (x, y, self.sideLength, self.sideLength))
        image.set_colorkey([0, 0, 0])
        return image

    def getImages(self, y: int) -> list[pygame.Surface]:
        """
        Create a list of all the images of the player depending on the direction (each direction is a different row)
        """
        images = []
        for i in range(0, 5):
            x = i * self.sideLength
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
    def __init__(self, name, sideLength):
        super().__init__(name, sideLength)
        self.image = self.getImage(0, 0)
        self.rect = self.image.get_rect()
        self.velocity = 5

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


class Player(Entity, pygame.sprite.Sprite):
    """
    Player class
    """

    def __init__(self, name, sideLength, screen):
        super().__init__(name, sideLength)
        # Get the center of the screen
        self.center = (screen.get_width() // 2, screen.get_height() // 2)
        # Get the half of the screen
        self.half = (screen.get_width() // 2, screen.get_height() // 2)
        self.bombGroup = pygame.sprite.Group()
        self.bx, self.by = 0, 0
        self.screen = screen
        self.maxHealth = 100
        self.bomb = ''
        self.health = self.maxHealth

    def drawHealthBar(self):
        """
        Draw the health bar
        """
        maxWidth = self.maxHealth * 2
        width = self.health * 2
        pygame.draw.rect(self.screen, (255, 0, 0), [0, 0, maxWidth, 20])
        pygame.draw.rect(self.screen, (0, 255, 0), [0, 0, width, 20])

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

    def checkCollision(self, entity):
        """
        Check if the player is colliding with an enemy
        """
        if self.rect.colliderect(entity.rect):
            self.damage(0.2)
            print(f"{self.health=}")


class Boss(Entity):
    """
    Boss class
    """

    def __init__(self, name, sideLength):
        super().__init__(name, sideLength)
        self.direction = "right"
        self.rockGroup = pygame.sprite.Group()

    def getPosition(self):
        return self.rect.x, self.rect.y

    def move(self, player):
        dx, dy = (player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        stepx, stepy = (dx / 25., dy / 25.)
        self.rect.x += stepx
        self.rect.y += stepy
