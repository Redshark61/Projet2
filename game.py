# pylint: disable=W0201
import pygame
from player import Player
from map import MapManager
from quest import Quest
from musics import Music


class Game:

    def __init__(self):
        # Initialize the screen
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Super jeu")
        # Initialize Musics
        self.stepMusic = Music()
        self.eventMusic = Music()
        self.playMusicOutdoor = Music()
        self.playMusicDungeon = Music()

    def initalize(self, choice=None):
        """
        Setup all the variables of the game
        """

        # Creation of the player if the choice is 'new' (selected from the menu)
        if choice == 'new':
            self.player = Player(
                self.screen, self, "Soldiers/Melee/AssasinTemplate")
        # Otherwise, load the player from the database
        else:
            self.player = Player(
                self.screen, self, hasToUpload=True, choice=choice)
        # Initialize the map
        self.map = MapManager(self, self.screen)

        # Teleport the player to the start of the map and save its location
        if choice == 'new':
            self.map.teleportPlayer("spawnPlayer")
            self.map.updateMonsterInDB()

            self.player.playerDB.updateValue()

    def handleInput(self):
        """
        Handle the player inputs
        """
        pressed = pygame.key.get_pressed()

        self.stepMusic.setVolume(0.1)
        if pressed[pygame.K_z]:
            self.player.moveUp()
            self.stepMusic.playIfReady("step1", 0)
        elif pressed[pygame.K_s]:
            self.player.moveDown()
            self.stepMusic.playIfReady("step1", 0)
        if pressed[pygame.K_q]:
            self.player.moveLeft()
            self.stepMusic.playIfReady("step1", 0)
        elif pressed[pygame.K_d]:
            self.player.moveRight()
            self.stepMusic.playIfReady("step1", 0)

    def run(self, startNewGame):
        """
        Main loop of the game
        """
        running = True
        if startNewGame:
            self.map.teleportPlayer("spawnPlayer")

        # Set the clock to 60fps
        clock = pygame.time.Clock()

        while running:

            # Handling the quit event
            for event in pygame.event.get():

                # If the player click
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # If the button to quit when you die exists
                    if self.map.quitButtonRect is not None:
                        if self.map.quitButtonRect.collidepoint(pygame.mouse.get_pos()):
                            return False
                    if self.map.returnButtonRect is not None:
                        return True

                    # If the player left click while in a dungeon
                    if 'donjon' in self.map.getMap().name.lower():
                        self.player.lauchProjectile()

                # If the player press the cross to quit
                if event.type == pygame.QUIT:
                    # Update the database
                    self.player.playerDB.updateValue()
                    self.map.updateMonsterInDB()
                    running = False

                if event.type == pygame.KEYDOWN:
                    # If the player press 'P'
                    if event.key == pygame.K_p:
                        # Hide the quest panel
                        Quest.hideQuestPanel()
                    # If the player press 'C'
                    elif event.key == pygame.K_c:
                        # Add life and xp to the player
                        self.player.maxHealth += 300
                        self.player.health = self.player.maxHealth
                        self.player.currentLevel += 5
                        self.eventMusic.play("cheat", 0)
                    # If the player press 'Escape'
                    elif event.key == pygame.K_ESCAPE:
                        # Save the game
                        self.player.playerDB.updateValue()
                        self.map.updateMonsterInDB()
                        self.eventMusic.play("save", 0)
                        print("Saving...")

            # Move every projectile
            for projectile in self.player.bombGroup:
                projectile.move()

            self.screen.fill((0, 0, 0))
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

            if "donjon" in self.map.getMap().name.lower():
                self.playMusicOutdoor.stopMusic()
                self.playMusicDungeon.playIfReady("dungeon", -1)
                self.playMusicDungeon.setVolume(0.05)
            else:
                self.playMusicDungeon.stopMusic()
                self.playMusicOutdoor.playIfReady("outdoor", -1)
                self.playMusicOutdoor.setVolume(0.05)

            pygame.display.update()
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()
