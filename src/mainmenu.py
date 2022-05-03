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

import pygame

from pygame         import Surface
from enum           import Enum

from src.events     import EventHandler
from src.colors     import Color
from src.assets     import Assets
from src.particle   import MainMenuParticleSystem


class MainMenuCursor(Enum):
    Play = 0
    Quit = 1


class MainMenuScreen(object):

    def __init__(self, screen : Surface, assets : Assets, event_handler : EventHandler) -> None:
        self.screen          : Surface                = screen
        self.assets          : Assets                 = assets
        self.events          : EventHandler           = event_handler

        self.particle_system : MainMenuParticleSystem = MainMenuParticleSystem()
        self.cursor          : MainMenuCursor         = MainMenuCursor.Play


    def render(self, delta : float) -> None:
        self.screen.fill(Color.LightBlack)

        self.particle_system.update(delta)
        for particle in self.particle_system.particles:
            pygame.draw.rect(self.screen, particle.color, (particle.position[0], particle.position[1], particle.size, particle.size), 1)

        self.screen.blit(self.assets.main_menu_background_image, (  0,  0))
        self.screen.blit(self.assets.main_menu_logo_image,       ( 80, 90))
        self.screen.blit(self.assets.main_menu_misaka_image,     (550,  0))

        if self.events.keys["up"]:
            self.assets.channel1.play(self.assets.select_sound)
            self.events.keys["up"] = False
            self.cursor = MainMenuCursor.Play

        if self.events.keys["down"]: 
            self.assets.channel2.play(self.assets.select_sound)
            self.events.keys["down"] = False
            self.cursor = MainMenuCursor.Quit

        self.screen.blit(
            self.assets.font_64.render(">> Play <<" if self.cursor == MainMenuCursor.Play else "   Play   ", True, 
            Color.LightGreen if self.cursor == MainMenuCursor.Play else Color.White), ( 200, 390 ))
        self.screen.blit(
            self.assets.font_64.render(">> Quit <<" if self.cursor == MainMenuCursor.Quit else "   Quit   ", True, 
            Color.LightRed   if self.cursor == MainMenuCursor.Quit else Color.White), ( 200, 460 ))