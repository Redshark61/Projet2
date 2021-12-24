import pygame
import menu
from musics import Music
import Variables as var


def shutSounds():

    if not menu.Menu.soundState:
        for i in range(Music.channelNumber):
            pygame.mixer.Channel(i).set_volume(0)
    else:
        for i in range(Music.channelNumber):
            pygame.mixer.Channel(i).set_volume(var.volume)
