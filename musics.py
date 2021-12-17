import pygame
from db.db import Database


class Music:

    channelNumber = 0
    pygame.mixer.init()
    sounds = {}
    results = Database.query("SELECT name, soundpath FROM sounds")
    for sound in results:
        sounds[sound[0]] = pygame.mixer.Sound(sound[1])

    def __init__(self):
        pygame.mixer.set_num_channels(20)

        # set a new channel for every new instance
        self.channel = pygame.mixer.Channel(self.channelNumber)
        Music.channelNumber += 1

    def play(self, soundName, loop):
        self.channel.play(self.sounds[soundName], loop)

    def playIfReady(self, soundName, loop):
        if not self.channel.get_busy():
            self.play(soundName, loop)

    def pause(self):
        self.channel.pause()

    def setVolume(self,volume):
        self.channel.set_volume(volume)

    def stopMusic(self):
        self.channel.stop()

