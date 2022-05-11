"""
---------------------------------------------------------------------------------------------------------------------------------------
@file       src/screens/gameplay.py
@author     Milos Milicevic (milosh.mkv@gmail.com)

@version    0.1
@date       2022-04-28
@copyright 	Copyright (c) 2022
    
Distributed under the MIT software license, see the accompanying file LICENCE or http://www.opensource.org/licenses/mit-license.php.
---------------------------------------------------------------------------------------------------------------------------------------
"""

from random import random
import pygame

from pygame         import Surface
from datetime       import date

from src.events     import EventHandler
from src.assets     import Assets
from src.systems    import GameplaySystem
from src.constants  import Constants
from src.colors     import Color
from src.particle   import BackgroundParticleSystem, HardDropParticleSystem
from src.states     import GlobalStates

from src.screens.screen import Screen

BSIZE = 32

class GameplayScreen(Screen):

    def __init__(self, surface: Surface, assets: Assets, event_handler: EventHandler) -> None:
        self.surface   : Surface = surface
        self.assets    : Assets  = assets
        self.events    : EventHandler = event_handler
        self.system    : GameplaySystem = GameplaySystem(event_handler, self.assets)
        self.particles : BackgroundParticleSystem = BackgroundParticleSystem(Constants.SCREEN_SIZE[0], Constants.SCREEN_SIZE[1])
        self.hard_drop_particles : HardDropParticleSystem = HardDropParticleSystem()

        self.new_block_remove_timer : float = 0
        self.block_in_row_to_remove : int   = 0


        self.board_offset_y : float = 0
        self.vel : float = 0


    def get_image_for_block(self, peace: int) -> Surface:
        return self.assets.block_images[peace - 2]

    def render(self, delta: float) -> None:
        self.surface.fill(Color.LightBlack)

        # self.surface.blit(self.assets.misaka_image, (200,0))
        if self.events.keys["space"]:
            self.particles.distort()
    
        self.system.update(delta)

        self.draw_clear_animation(delta)
        
        # self.move_board(delta)
        self.particles.update(delta)
        self.particles.render(self.surface)
        self.hard_drop_particles.update(delta)
        self.hard_drop_particles.render(self.surface)

        self.draw_tetris_field(offset=13)
        self.draw_next_block(24)
        self.draw_hold_block(7)
        self.draw_info_board()
        self.draw_pause()

    def move_board(self, delta : float) -> None:
        if self.system.is_dropped_hard():
            self.vel = 10

        self.board_offset_y += self.vel * delta  * 2
        self.vel += -5 * delta * 15

        if self.board_offset_y < 0: self.board_offset_y = 0
        if self.board_offset_y > 5: self.board_offset_y = 5

    def draw_clear_animation(self, delta : float) -> None:
        if self.system.clear_time:
            self.new_block_remove_timer += delta

            if self.new_block_remove_timer > 0.04:
                self.new_block_remove_timer = 0
                
                for row in self.system.indices:
                    self.system.tetris_field[row][self.block_in_row_to_remove] = 0
                
                self.block_in_row_to_remove += 1


                if self.block_in_row_to_remove == Constants.COLS:
                    self.block_in_row_to_remove = 0
                    if len(self.system.indices) == 4:
                        self.particles.boom()
                    self.system.clear()

                   

    def draw_tetris_field(self, offset: int) -> None:
        pygame.draw.rect(self.surface, Color.Grey, (BSIZE * offset - 2, BSIZE - 2 + self.board_offset_y, BSIZE * 10 + 4, BSIZE * 20 + 4), 1)

        for i in range(Constants.ROWS):
            for j in range(Constants.COLS):
                if self.system.tetris_field[i][j]:
                    self.surface.blit(self.get_image_for_block(self.system.tetris_field[i][j]), ((j + offset) * BSIZE, i * BSIZE + self.board_offset_y))

        peace = self.system.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j] == 1 and not self.system.clear_time:
                    if (self.system.cursor[Constants.Y] + i) * BSIZE + self.board_offset_y >= BSIZE:
                        self.surface.blit(
                            self.get_image_for_block(Constants.VALUES[self.system.current_peace]), (
                                (self.system.cursor[Constants.X] +
                                j + offset) * BSIZE ,
                                (self.system.cursor[Constants.Y] + i) * BSIZE + self.board_offset_y))
                    self.surface.blit(self.assets.block_images[7], (
                        (self.system.ghost_cursor[Constants.X] +
                         j + offset) * BSIZE ,
                        (self.system.ghost_cursor[Constants.Y] + i) * BSIZE - BSIZE + self.board_offset_y))

        self.surface.blit(self.assets.logo_image, (BSIZE * 7, BSIZE * 1.5))

    def draw_info_board(self) -> None:

        self.surface.blit(self.assets.font_32.render(
            "Level", True, Color.Grey), (BSIZE * 24+8, 560))
        self.surface.blit(self.assets.font_32.render(
            ":", True, Color.Grey), (BSIZE * 24 + 8 + 90, 560))
        self.surface.blit(self.assets.font_32.render(
            str(self.system.level), True, Color.LightRed), (BSIZE * 24+8 + 110, 560))

        self.surface.blit(self.assets.font_32.render(
            "Lines", True, Color.Grey), (BSIZE * 24+8, 590))
        self.surface.blit(self.assets.font_32.render(
            ":", True, Color.Grey), (BSIZE * 24+8 + 90, 590))
        self.surface.blit(self.assets.font_32.render(
            str(self.system.cleared_lines), True, Color.LightRed), (BSIZE * 24+8 + 110, 590))

        self.surface.blit(self.assets.font_32.render(
            "Time", True, Color.Grey), (BSIZE * 24+8, 620))
        self.surface.blit(self.assets.font_32.render(
            ":", True, Color.Grey), (BSIZE * 24+8 + 90, 620))
        self.surface.blit(self.assets.font_32.render("{}:{}".format(int(self.system.total_time // 60), int(self.system.total_time % 60)),
                                                 True, Color.LightBlue), (BSIZE * 24 + 8 + 110, 620))

        self.draw_score()

    def draw_next_block(self, offset: int) -> None:
        self.draw_block(self.system.get_next_peace(), self.system.next_peace, offset)
        self.surface.blit(self.assets.font_32.render("Next", True, Color.Grey), (BSIZE * offset + 8, BSIZE * 5))

    def draw_hold_block(self, offset: int) -> None:
        self.draw_block(self.system.get_hold_peace(),
                        self.system.hold_peace, offset)
        self.surface.blit(self.assets.font_32.render("Hold", True, Color.Grey), (BSIZE * offset + 8, BSIZE * 5))

    def draw_block(self, peace: list, block_name: str, offset: int) -> None:
        pygame.draw.rect(self.surface, Color.Grey, (offset * 32, 5 * 32, 32 * 5, 32 * 4), 1)
        if not peace:
            return

        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j]:
                    self.surface.blit(self.get_image_for_block(Constants.VALUES[block_name]),
                                     ((j + offset) * BSIZE + Constants.BLOCK_DISPLAY_OFFSETS_X[block_name],
                                      ((i + 4) * BSIZE) + Constants.BLOCK_DISPLAY_OFFSETS_Y[block_name]))

    def draw_score(self) -> None:

        score = str(self.system.score)
        while len(score) < 9:
            score = "0" + score

        pygame.draw.rect(self.surface, Color.Grey, (BSIZE * 24,
                         BSIZE * 2, BSIZE * 5, BSIZE * 2), 1)
        self.surface.blit(self.assets.font_32.render(
            "Best", True, Color.Grey),      (BSIZE * 24 + 8, BSIZE * 2 + 2))
        self.surface.blit(self.assets.font_32.render(
            score, True, Color.LightRed),   (BSIZE * 24 + 8, BSIZE * 3))

        pygame.draw.rect(self.surface, Color.Grey, (BSIZE * 24,
                         BSIZE * 10, BSIZE * 5, BSIZE * 2), 1)
        self.surface.blit(self.assets.font_32.render(
            "Score", True, Color.Grey),     (BSIZE * 24 + 8, BSIZE * 10 + 2))
        self.surface.blit(self.assets.font_32.render(
            score, True, Color.LightGreen), (BSIZE * 24 + 8, BSIZE * 11))

    def draw_pause(self) -> None:
        if self.system.paused:
            pygame.draw.rect(self.surface, (40, 40, 40),
                             (8 * BSIZE, 250, 10 * 32, 200))
            self.surface.blit(self.text["Pause"],
                             (8 * BSIZE + 3 * 32 + 12, 310))
            self.surface.blit(self.text["Pause1"], (8 * BSIZE + 20, 360))
