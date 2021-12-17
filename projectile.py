import pygame


class Projectile(pygame.sprite.Sprite):

    def __init__(self, player, name: str, destinationPoint: list[int, int], screen: pygame.Surface):
        super().__init__()
        # get the center of the screen
        self.center = (screen.get_width() // 2, screen.get_height() // 2)

        self.player = player
        self.destinationPoint = destinationPoint

        # Set the begining position of the projectile
        self.beginPos = (self.player.rect.x) * \
            (1.75), (self.player.rect.y)*(1.75)

        # Set the sprite of the projectile
        self.spriteSheet = pygame.image.load(f"./assets/Objects/{name}.png")
        self.image = pygame.Surface([16, 16]).convert_alpha()
        self.image.blit(self.spriteSheet, (0, 0), (0, 0, 16, 16))
        self.rect = self.image.get_rect()

        # Scale up the image
        self.image = pygame.transform.scale(
            self.image, (self.rect.width * 2, self.rect.height * 2))
        self.image.set_colorkey((0, 0, 0))
        self.lengthMoved = 0
        self.rect.x = self.beginPos[0]
        self.rect.y = self.beginPos[1]

    def move(self):
        """
        Move the projectile to the destination point (mouse position)
        """
        dx, dy = (self.destinationPoint[0] - self.beginPos[0],
                  self.destinationPoint[1] - self.beginPos[1])
        stepx, stepy = (dx / 25., dy / 25.)
        self.rect.x += stepx
        self.rect.y += stepy
        if self.lengthMoved >= 25:
            self.remove()
        self.lengthMoved += 1

    def remove(self):
        """
        Kill the projectile
        """
        self.player.bombGroup.remove(self)
