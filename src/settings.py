"""
---------------------------------------------------------------------------------------------------------------------------------------
@file       settings.py
@author     Milos Milicevic (milosh.mkv@gmail.com)

@version    0.1
@date       2022-04-28
@copyright 	Copyright (c) 2022
    
Distributed under the MIT software license, see the accompanying file LICENCE or http://www.opensource.org/licenses/mit-license.php.
---------------------------------------------------------------------------------------------------------------------------------------
"""

from typing import Set
from pygame         import Surface
from src.particle   import BackgroundParticleSystem
from src.colors     import Color
from src.assets     import Assets
from src.events     import EventHandler
from enum           import Enum

from src.states import GlobalStates


class Settings:
    Level : int  = 0
    Music : bool = False
    Sound : bool = True
class SettingsCursor(Enum):
    Level = 0
    Music = 1
    Sound = 2
    Back  = 3

class SettingsScreen(object):

    def __init__(self, screen : Surface, assets : Assets, event_handler : EventHandler) -> None:
        self.screen    : Surface                  = screen
        self.assets    : Assets                   = assets
        self.events    : EventHandler             = event_handler

        self.cursor    : SettingsCursor           = SettingsCursor.Level
        self.particles : BackgroundParticleSystem = BackgroundParticleSystem()


    def render(self, delta : float) -> None:
        self.screen.fill(Color.LightBlack)

        self.particles.update(delta)
        self.particles.render(self.screen)

        self.screen.blit(self.assets.logo_image, (32, 32))


        if self.events.key("down"):
            if Settings.Level > 4:
                self.cursor = SettingsCursor.Back if self.cursor.value + 1 > SettingsCursor.Back.value else SettingsCursor(self.cursor.value + 1)
            else:
                Settings.Level += 5
            self.assets.channel1.play(self.assets.select_sound)

        if self.events.key("up"):
            if Settings.Level < 5:
                pass
            else:
                Settings.Level -= 5
            self.cursor = SettingsCursor(self.cursor.value - 1)
            self.assets.channel1.play(self.assets.select_sound)

        if self.cursor == SettingsCursor.Level and self.events.key("left"):
            if Settings.Level == 0:
                return
            Settings.Level -= 1
            self.assets.channel1.play(self.assets.select_sound)

        if self.cursor == SettingsCursor.Level and self.events.key("right"):
            if Settings.Level == 9:
                return
            Settings.Level += 1
            self.assets.channel1.play(self.assets.select_sound)

        

        if self.cursor == SettingsCursor.Back and self.events.key("enter"):
            GlobalStates.Screen = "MainMenu"
            self.assets.channel1.play(self.assets.enter_sound)

        if self.cursor == SettingsCursor.Back and self.events.key("up"):
            self.cursor = SettingsCursor.Level
            self.assets.channel1.play(self.assets.select_sound)

        

        self.screen.blit(self.assets.font.render(str(">> Starting Level <<" if self.cursor == SettingsCursor.Level else "   Starting Level   "), True, Color.Grey), (105, 160))
        for i in range(2):
            for j in range(5):
                color = Color.White
                if Settings.Level == ( i * 5 ) + j:
                    color = Color.LightGreen
                    self.screen.blit(self.assets.settings_level_cursor, (82 + 64 * j  , i * 64 + 208))
                self.screen.blit(self.assets.font_64.render(str( ( i * 5 ) + j ), True, color), (100 + j * 64, 210 + i * 64))

        
        self.screen.blit(self.assets.font.render("Audio", True, Color.Grey), (195, 400))
        if self.events.key("space"):
            Settings.Music = not Settings.Music
        music_str = "Music: " + ("On" if Settings.Music else "Off")
        sound_str = "Sound: " + ("On" if Settings.Sound else "Off") 

        self.screen.blit(self.assets.font.render(">> "+music_str+" <<" if self.cursor == SettingsCursor.Music else "   "+music_str+"   ", True, Color.White), (135, 450))
        self.screen.blit(self.assets.font.render(">> "+sound_str+" <<" if self.cursor == SettingsCursor.Sound else "   "+sound_str+"   ", True, Color.White), (135, 500))

        self.screen.blit(self.assets.font_48.render(str( ">> Back <<" if self.cursor == SettingsCursor.Back else "   Back   " ), True, Color.Grey), ( 64, 620))
