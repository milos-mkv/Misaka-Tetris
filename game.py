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
import pickle

from pygame                import Surface
from pygame.time           import Clock
from src.colors            import Color
from src.constants         import Constants
from src.assets            import Assets
from src.events            import EventHandler
from src.settings          import Settings
from src.screens.gameplay  import GameplayScreen
from src.states            import GlobalStates

class Game(object):

    def __init__(self) -> None:
        self.surface       : Surface      = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF)
        self.clock         : Clock        = pygame.time.Clock()
        self.delta         : float        = 0
        self.assets        : Assets       = Assets()
        self.event_handler : EventHandler = EventHandler()

        self.screens : dict = {
            "Gameplay": GameplayScreen(self.surface, self.assets, self.event_handler)
        }

        pygame.display.set_caption('Misaka Tetris')
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))


    def run(self) -> None:
        while GlobalStates.Running:
            self.delta = self.clock.tick() / 1000.0
            
            self.poll_events()      
            self.surface.fill(Color.LightBlack)

            self.screens[GlobalStates.Screen].render(self.delta)

            pygame.display.flip()


    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:    GlobalStates.Running = False
            if event.type == pygame.KEYDOWN: self.event_handler.handle_key_events(event, True )
            if event.type == pygame.KEYUP:   self.event_handler.handle_key_events(event, False)


if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mixer.init()
    pygame.joystick.init()

    game = Game()
    game.run()

    pygame.quit()
    pygame.mixer.quit()
    pygame.joystick.quit()