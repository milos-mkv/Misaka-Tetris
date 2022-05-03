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

from pygame     import Surface
from src.particle import MainMenuParticleSystem
from src.colors import Color
from src.assets import Assets
from src.events import EventHandler
from enum       import Enum

import pygame


class SettingsCursor(Enum):
    Start = 0
    Level = 1


class SettingsScreen(object):

    def __init__(self, screen : Surface, assets : Assets, event_handler : EventHandler) -> None:
        self.screen          : Surface                = screen
        self.assets          : Assets                 = assets
        self.events          : EventHandler           = event_handler
        self.cursor          : SettingsCursor         = SettingsCursor.Start
        self.particle_system : MainMenuParticleSystem = MainMenuParticleSystem()

    def render(self, delta : float) -> None:
        self.screen.fill(Color.LightBlack)

        self.particle_system.update(delta)
        for particle in self.particle_system.particles:
            pygame.draw.rect(self.screen, particle.color, (particle.position[0], particle.position[1], particle.size, particle.size))

        self.screen.blit(self.assets.settings_background_image, (0, 0))
        self.screen.blit(self.assets.logo_image, (32, 32))
        self.screen.blit(self.assets.font.render(str( "Starting Level" ), True, Color.LightBlue), ( 40, 260))

        for i in range(2):
            for j in range(5):
                self.screen.blit(self.assets.font_64.render(str( ( i * 5 ) + j ), True, Color.White), (80 + j * 64, 310 + i * 64))

        self.screen.blit(self.assets.settings_level_cursor, (63, 208))
        self.screen.blit(self.assets.font_64.render(str( "PLAY" ), True, Color.White), ( 64, 500))
