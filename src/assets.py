
import pygame

from pygame.mixer import Channel
from pygame       import Surface

class Assets(object):

    def __init__(self) -> None:
        self.init_video()
        self.init_audio()
        self.init_fonts()
       
    def init_video(self) -> None:

        self.main_menu_logo_image       : Surface = pygame.image.load("./assets/main_menu_logo.png").convert_alpha()
        self.main_menu_misaka_image     : Surface = pygame.image.load("./assets/misaka3.png"       ).convert_alpha()

        self.settings_background_image  : Surface = pygame.transform.scale(pygame.image.load("./assets/settings4.png"  ).convert_alpha() ,(1227, 700) )

        self.logo_image       : Surface = pygame.image.load("./assets/Untitled.png").convert_alpha()
        self.misaka_image     : Surface = pygame.transform.scale(pygame.image.load("./assets/mil.png" ).convert_alpha(), (1150, 710))

        self.block_images     : list    = []
        for i in range(1, 10):
            self.block_images.append(pygame.image.load("./assets/blocks/" + str(i) +".png").convert_alpha())




    def init_audio(self) -> None:
        self.channel1 : Channel = pygame.mixer.Channel(0)
        self.channel2 : Channel = pygame.mixer.Channel(1)

        self.drop_sound  = pygame.mixer.Sound("./assets/drop.wav" ) 
        self.bg_music    = pygame.mixer.Sound("./assets/bg1.mp3" ) 
        self.clear_sound = pygame.mixer.Sound("./assets/clear.mp3") 
        self.select_sound = pygame.mixer.Sound("./assets/select.wav") 
        self.enter_sound = pygame.mixer.Sound("./assets/enter.wav") 
        self.enter_sound.set_volume(0.09)
        self.drop_sound.set_volume(0.1)
        self.select_sound.set_volume(0.08)
        self.clear_sound.set_volume(0.08)

    def init_fonts(self) -> None:
        self.font_24 = pygame.font.Font('./assets/font.ttf', 24)
        self.font_32 = pygame.font.Font('./assets/font.ttf', 32)
        self.font_48 = pygame.font.Font('./assets/font.ttf', 48)
        self.font_64 = pygame.font.Font('./assets/font.ttf', 64)
        self.font_consolas = pygame.font.Font('./assets/font1.ttf', 12)