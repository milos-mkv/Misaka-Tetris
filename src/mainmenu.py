"""
---------------------------------------------------------------------------------------------------------------------------------------
@file       game.py
@author     Milos Milicevic (milosh.mkv@gmail.com)

@version    0.1
@date       2022-04-28
@copyright 	Copyright (c) 2022
    
Distributed under the MIT software license, see the accompanying file LICENCE or http://www.opensource.org/licenses/mit-license.php.
---------------------------------------------------------------------------------------------------------------------------------------
"""

from pygame         import Surface
from enum           import Enum

from src.events     import EventHandler
from src.colors     import Color
from src.assets     import Assets
from src.particle   import BackgroundParticleSystem
from src.states     import GlobalStates


class MainMenuCursor(Enum):
    Play     = 0
    Settings = 1
    Quit     = 2


class MainMenuScreen(object):

    def __init__(self, screen : Surface, assets : Assets, event_handler : EventHandler) -> None:
        self.screen    : Surface                  = screen
        self.assets    : Assets                   = assets
        self.events    : EventHandler             = event_handler

        self.particles : BackgroundParticleSystem = BackgroundParticleSystem(100, 100)
        self.cursor    : MainMenuCursor           = MainMenuCursor.Play


    def render(self, delta : float) -> None:
        self.screen.fill(Color.LightBlack)

        self.particles.update(delta)
        self.particles.render(self.screen)

        self.screen.blit(self.assets.main_menu_logo_image,   ( 80, 90))
        self.screen.blit(self.assets.main_menu_misaka_image, (550,  0))

        if self.events.key("up"):
            if self.cursor == MainMenuCursor.Play:
                return
            self.cursor = MainMenuCursor(self.cursor.value - 1)
            self.assets.channel1.play(self.assets.select_sound)

        if self.events.key("down"): 
            if self.cursor == MainMenuCursor.Quit:
                return
            self.cursor = MainMenuCursor(self.cursor.value + 1)
            self.assets.channel2.play(self.assets.select_sound)

        if self.events.key("enter"):
            self.assets.channel1.play(self.assets.enter_sound)
            if self.cursor == MainMenuCursor.Play:     GlobalStates.Screen  = "Gameplay"
            if self.cursor == MainMenuCursor.Settings: GlobalStates.Screen  = "Settings"
            if self.cursor == MainMenuCursor.Quit:     GlobalStates.Running = False

        self.draw_text("Play",     (200, 390), MainMenuCursor.Play    )
        self.draw_text("Settings", (140, 460), MainMenuCursor.Settings)
        self.draw_text("Quit",     (200, 530), MainMenuCursor.Quit    )

        self.screen.blit(self.assets.font_consolas.render("Developed by Milos Milicevic", True, Color.Grey), (10, 680))


    def draw_text(self, text : str, position : tuple, cursor : MainMenuCursor) -> None:
        self.screen.blit(self.assets.font_64.render(">> " + text + " <<" if self.cursor == cursor else "   " + text + "   ", 
            True, Color.LogoRed if self.cursor == cursor else Color.White), position)