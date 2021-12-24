import pygame
import menu
from musics import Music
import Variables as var


def shutSounds():

    # Set the volume to 0 if the state is False
    sfxVolume = 0 if not menu.Menu.soundStateSfx else var.volumeSfx
    # Lower the volume of the sfx
    for sound in Music.sfxSound:
        pygame.mixer.Channel(sound.channelNumber).set_volume(sfxVolume)

    # Set the volume to 0 if the state is False
    ambientVolume = 0 if not menu.Menu.soundStateAmbient else var.volumeAmbient
    # Lower the volume of the ambient
    for sound in Music.ambientSound:
        pygame.mixer.Channel(sound.channelNumber).set_volume(ambientVolume)


def setVolume():
    # Set the volume for every sounds (even the new ones)
    for sound in Music.sfxSound:
        pygame.mixer.Channel(sound.channelNumber).set_volume(var.volumeSfx)
    for sound in Music.ambientSound:
        pygame.mixer.Channel(sound.channelNumber).set_volume(var.volumeAmbient)
