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

from pygame        import Surface
from pygame.time   import Clock

from src.constants import Constants
from src.assets    import Assets
from src.events    import EventHandler
from src.systems   import GameplaySystem
from src.settings  import SettingsScreen
from src.renderer  import Renderer

from src.mainmenu  import MainMenuCursor, MainMenuScreen

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
pygame.joystick.init()

from enum import Enum

class Screen(Enum):
    MainMenu = 0
    Settings = 1
    Gameplay = 2

class Game(object):

    def __init__(self) -> None:
        """
        Function: __init__
        """

        self.screen  : Surface = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF)
        self.clock   : Clock   = pygame.time.Clock()
        self.running : bool    = True
        self.delta   : float   = 0

        self.event_handler   : EventHandler   = EventHandler()
        self.assets          : Assets         = Assets()
        self.gameplay_system : GameplaySystem = GameplaySystem(self.event_handler, self.assets)
        self.renderer        : Renderer       = Renderer(self.screen, self.assets, self.gameplay_system)

        self.main_menu_screen : MainMenuScreen = MainMenuScreen(self.screen, self.assets, self.event_handler)
        self.settings_screen  : SettingsScreen = SettingsScreen(self.screen, self.assets, self.event_handler)

        self.current_screen   : Screen = Screen.MainMenu

        # self.assets.bg_music.set_volume(0.01)
        # self.assets.channel2.play(self.assets.bg_music)
                                
        pygame.display.set_caption('Misaka Tetris')
        pygame.display.set_icon(pygame.image.load("./assets/icon.png"))


    def run(self) -> None:
        """
        Function: run

        Brief:
            Run game loop.
        """

        second_counter : int = 0

        while self.running:
            self.delta = self.clock.tick() / 1000.0

            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:    self.running = False
                if event.type == pygame.KEYDOWN: 
                    self.event_handler.handle_key_events(event, True )
                    if event.key == pygame.K_RETURN:
                        self.gameplay_system.paused = not self.gameplay_system.paused
                if event.type == pygame.KEYUP:   
                    self.event_handler.handle_key_events(event, False)
                self.event_handler.handle_joystick_buttons(event)
     



            if self.screen == Screen.Gameplay:
                self.gameplay_system.update(self.delta)
                self.renderer.render(self.delta)
            elif self.screen == Screen.Settings:
                self.settings_screen.render(self.delta)
            else:
                self.main_menu_screen.render(self.delta)
                if self.event_handler.keys["enter"] and self.main_menu_screen.cursor == MainMenuCursor.Quit:
                    self.running = False
                if self.event_handler.keys["enter"] and self.main_menu_screen.cursor == MainMenuCursor.Play:
                    self.screen = Screen.Gameplay
            pygame.display.flip()
            
            second_counter += self.delta

            if second_counter >= 1.0:
                print(self.clock.get_fps())
                second_counter = 0

if __name__ == "__main__":
    game = Game()
    game.run()

    pygame.quit()
    pygame.mixer.quit()
    pygame.joystick.quit()