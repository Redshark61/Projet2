import pygame

class Music:

    channelNumber = 0
    pygame.mixer.init()

    def __init__(self):
        pygame.mixer.set_num_channels(20)
        self.channel = pygame.mixer.Channel(self.channelNumber)

        Music.channelNumber += 1
        
        self.sounds = {
            "outdoor" : pygame.mixer.Sound("assets/musics/music_outdoor.wav"),
            "dungeon" : pygame.mixer.Sound("assets/musics/music_dungeon.wav"),
            "menuMusic" : pygame.mixer.Sound("assets/musics/menuMusic.wav"),
            "loading" : pygame.mixer.Sound("assets/musics/loading.wav"),
            "step1" : pygame.mixer.Sound("assets/musics/Footsteps_Casual_Earth_01.wav"),
            "fireball" : pygame.mixer.Sound("assets/musics/fire_ball.wav"),
            "cheat" : pygame.mixer.Sound("assets/musics/omg.wav"),
            "hitEnemy" : pygame.mixer.Sound("assets/musics/hit_enemy.wav"),
            "dungeonWin" : pygame.mixer.Sound("assets/musics/fin_donjon.wav"),
            "save" : pygame.mixer.Sound("assets/musics/menuMusics/FileSave.wav"),
            "levelUp" : pygame.mixer.Sound("assets/musics/dungeon_win.wav")
        }

    def play(self, soundName, loop):
        self.channel.play(self.sounds[soundName], loop)
        
    def playIfReady(self, soundName, loop):
        if not self.channel.get_busy():
            self.play(soundName, loop)

    def pause(self):
        self.channel.pause()

    def setVolume(self):
        self.channel.set_volume(0)

    def stopMusic(self):
        self.channel.stop()   
    # 
    # self.winDungeonMusic.play("dungeonWin",0)
    # self.menuMusic.setVolume()