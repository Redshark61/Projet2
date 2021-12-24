import pygame
from db.db import Database
import Variables as var


class Music:

    channelNumber = 0
    pygame.mixer.init()

    # Create an empty dictionary of sounds
    sounds = {}

    # Load all sounds in the sounds dictionary
    results = Database.query("SELECT name, soundpath FROM sounds")
    for sound in results:
        sounds[sound[0]] = pygame.mixer.Sound(sound[1])

    ambientSound = []
    sfxSound = []

    def __init__(self, again=False, isAmbient=False):
        pygame.mixer.set_num_channels(20)
        if again:
            Music.channelNumber = 0
        self.channelNumber = Music.channelNumber
        # set a new channel for every new instance
        self.channel = pygame.mixer.Channel(self.channelNumber)
        self.setVolume(var.volume)

        # If the music is ambient, then add it to the ambientSound list
        if isAmbient:
            Music.ambientSound.append(self)
        else:
            Music.sfxSound.append(self)
        Music.channelNumber += 1

    def play(self, soundName, loop):
        self.channel.play(self.sounds[soundName], loop)

    def playIfReady(self, soundName, loop):
        if not self.channel.get_busy():
            self.play(soundName, loop)

    def pause(self):
        self.channel.pause()

    def setVolume(self, volume):
        self.channel.set_volume(volume)

    def stopMusic(self):
        self.channel.stop()
