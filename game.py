import time
import pygame
from pygame.constants import MOUSEBUTTONDOWN
from player import Boss, Player
from map import MapManager


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Pygamon - aventure")
        self.player = Player("Soldiers/Melee/AssasinTemplate", 16, self.screen)
        self.boss = Boss("Monsters/Demons/RedDemon", 16)
        self.ax, self.ay = self.player.rect.x, self.player.rect.y
        self.map = MapManager(self, [self.player, self.boss])
        self.map.teleportPlayer("spawnPlayer", self.player)
        self.map.teleportPlayer("spawnBoss", self.boss)
        self.bossSpawn = self.boss.getPosition()
        self.isLaunched = False

    def handleInput(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.moveUp()
        elif pressed[pygame.K_DOWN]:
            self.player.moveDown()
        elif pressed[pygame.K_LEFT]:
            self.player.moveLeft()
        elif pressed[pygame.K_RIGHT]:
            self.player.moveRight()

    def run(self):
        running = True

        # Set the clock to 60fps
        clock = pygame.time.Clock()
        lastTime = time.time()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == MOUSEBUTTONDOWN:
                    self.player.lauchProjectile()

            for projectile in self.player.bombGroup:
                projectile.move()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.boss.image, self.boss.rect)
            self.handleInput()
            # Wait for 5seconds
            if lastTime + 2 < time.time():
                pass
            self.boss.move(self.player)
            self.boss.changeAnimation('down')
            self.map.updateMap()
            self.map.drawMap()
            self.player.checkCollision(self.boss)
            self.player.drawHealthBar()
            self.player.bombGroup.draw(self.screen)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()
