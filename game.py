import pygame
from pygame.constants import MOUSEBUTTONDOWN
from player import Player
from map import MapManager
from quest import Quest


class Game:

    def __init__(self):
        # Initialize the screen
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Super jeu")
        # Creation of the player
        self.player = Player("Soldiers/Melee/AssasinTemplate",  self.screen)
        # The target for the boss
        self.ax, self.ay = self.player.rect.x, self.player.rect.y
        # Initialize the map
        self.map = MapManager(self, self.screen)
        # Teleport the player to the start of the map
        self.map.teleportPlayer("spawnPlayer")
        # self.isLaunched = False

    def handleInput(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            self.player.moveUp()
        elif pressed[pygame.K_s]:
            self.player.moveDown()
        if pressed[pygame.K_q]:
            self.player.moveLeft()
        elif pressed[pygame.K_d]:
            self.player.moveRight()

    def run(self):
        running = True

        # Set the clock to 60fps
        clock = pygame.time.Clock()

        while running:
            # Handling the quit event
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.map.quitButtonRect is not None :
                        if self.map.quitButtonRect.collidepoint(pygame.mouse.get_pos()):
                           running = False
                if event.type == pygame.QUIT:
                    running = False

                # If the player left click
                if event.type == MOUSEBUTTONDOWN and 'donjon' in self.map.getMap().name:
                    self.player.lauchProjectile()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        Quest.hideQuestPanel()
                    elif event.key == pygame.K_c:
                        self.player.maxHealth += 300
                        self.player.health = self.player.maxHealth
                        self.player.currentLevel += 5

            # Move every projectile
            for projectile in self.player.bombGroup:
                projectile.move()

            self.screen.fill((0, 0, 0))
            # Display the player
            self.screen.blit(self.player.image, self.player.rect)
            # Save its previous location
            self.player.saveLocation()
            self.handleInput()
            # Update the map
            self.map.updateMap()
            # Draw the map
            self.map.drawMap()
            # Draw the health bar
            self.player.drawHealthBar()
            # Draw the xp bar
            self.player.drawLevelBar()
            # Draw the projectiles
            self.player.bombGroup.draw(self.screen)
            # make the player respawn when health drop to 0
            self.map.respawn()

            pygame.display.update()
            pygame.display.flip()
            clock.tick(60)
    pygame.quit()
