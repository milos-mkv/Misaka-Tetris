

from pygame import Surface
import pygame
from src.events import EventHandler

from src.assets import Assets
from src.systems import GameplaySystem
from src.constants import Constants
from src.colors import Color
from src.particle import BackgroundParticleSystem

from src.states import GlobalStates
from datetime import date
BSIZE = 32


class GameplayScreen(object):

    def __init__(self, screen: Surface, assets: Assets, event_handler: EventHandler) -> None:

        self.screen: Surface = screen
        self.assets: Assets = assets
        self.system: GameplaySystem = GameplaySystem(
            event_handler, self.assets)
        self.particles: BackgroundParticleSystem = BackgroundParticleSystem(100, 100)
        self.init_text()
        self.back = pygame.Surface((10 * 32, 20 * 32))
        self.back.fill(Color.LightBlack)
        self.back.set_alpha(220)

        # self.ps = HardDropParticles()

    def init_text(self) -> None:
        self.text: dict = {
            "Hold":  self.assets.font_32.render("Hold",  True, Color.Grey),
            "Next":  self.assets.font_32.render("Next",  True, Color.Grey),
            "Lines": self.assets.font_32.render("Lines", True, Color.White),
            ":":     self.assets.font_32.render(":",     True, Color.White),
            "Play":  self.assets.font_32.render("Play",  True, Color.White),
            "Time":  self.assets.font_32.render("Time",  True, Color.White),
            "Pause": self.assets.font_48.render("Pause", True, Color.White),
            "Pause1": self.assets.font_32.render("Press [P] to unpause", True, Color.White),
        }

    def get_image_for_block(self, peace: int) -> Surface:
        return self.assets.block_images[peace - 2]

    def render(self, delta: float) -> None:
        self.screen.fill(Color.LightBlack)
        self.system.update(delta)

 

        if self.system.pause_time > 0:
            self.system.pause_time -= delta

        if len(self.system.indices) > 0:
            self.system.indices = []
            self.system.pause_time = 0.5

        self.particles.update(delta)
        self.particles.render(self.screen)

        if self.system.is_dropped_hard():
            cur = [self.system.dropped_hard_cursor[0] * BSIZE + 13 *BSIZE,
                self.system.dropped_hard_cursor[1] * BSIZE
            ]
            print(cur)
            self.ps.add(cur)

        self.ps.update(delta)
        self.ps.render(self.screen)


        self.draw_tetris_field(offset=13)
        self.draw_next_block(24)
        self.draw_hold_block(7)
        self.draw_info_board()
        self.draw_pause()

        d = str(date.today())

    def draw_tetris_field(self, offset: int) -> None:
        # self.screen.blit(self.back, (BSize * offset, BSize ))
        pygame.draw.rect(self.screen, Color.Grey, (BSIZE * offset - 2,
                         BSIZE - 2, BSIZE * 10 + 4, BSIZE * 20 + 4), 1)

        for i in range(Constants.ROWS):
            for j in range(Constants.COLS):
                if self.system.tetris_field[i][j]:
                    self.screen.blit(self.get_image_for_block(
                        self.system.tetris_field[i][j]), ((j + offset) * BSIZE, i * BSIZE))

        peace = self.system.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j] == 1 and self.system.pause_time <= 0:
                    self.screen.blit(
                        self.get_image_for_block(Constants.VALUES[self.system.current_peace]), (
                            (self.system.cursor[Constants.X] +
                             j + offset) * BSIZE,
                            (self.system.cursor[Constants.Y] + i) * BSIZE))
                    self.screen.blit(self.assets.block_images[7], (
                        (self.system.ghost_cursor[Constants.X] +
                         j + offset) * BSIZE,
                        (self.system.ghost_cursor[Constants.Y] + i) * BSIZE - BSIZE))

        self.screen.blit(self.assets.logo_image, (BSIZE * 7, BSIZE * 1.5))

    def draw_info_board(self) -> None:

        self.screen.blit(self.assets.font_32.render(
            "Level", True, Color.Grey), (BSIZE * 24+8, 560))
        self.screen.blit(self.assets.font_32.render(
            ":", True, Color.Grey), (BSIZE * 24 + 8 + 90, 560))
        self.screen.blit(self.assets.font_32.render(
            str(self.system.level), True, Color.LightRed), (BSIZE * 24+8 + 110, 560))

        self.screen.blit(self.assets.font_32.render(
            "Lines", True, Color.Grey), (BSIZE * 24+8, 590))
        self.screen.blit(self.assets.font_32.render(
            ":", True, Color.Grey), (BSIZE * 24+8 + 90, 590))
        self.screen.blit(self.assets.font_32.render(
            str(self.system.cleared_lines), True, Color.LightRed), (BSIZE * 24+8 + 110, 590))

        self.screen.blit(self.assets.font_32.render(
            "Time", True, Color.Grey), (BSIZE * 24+8, 620))
        self.screen.blit(self.assets.font_32.render(
            ":", True, Color.Grey), (BSIZE * 24+8 + 90, 620))
        self.screen.blit(self.assets.font_32.render("{}:{}".format(int(self.system.total_time // 60), int(self.system.total_time % 60)),
                                                 True, Color.LightBlue), (BSIZE * 24 + 8 + 110, 620))

        self.draw_score()

    def draw_next_block(self, offset: int) -> None:
        self.draw_block(self.system.get_next_peace(),
                        self.system.next_peace, offset)
        self.screen.blit(self.text["Next"], (BSIZE * offset + 5, BSIZE * 5))

    def draw_hold_block(self, offset: int) -> None:
        self.draw_block(self.system.get_hold_peace(),
                        self.system.hold_peace, offset)
        self.screen.blit(self.text["Hold"], (BSIZE * offset + 5, BSIZE * 5))

    def draw_block(self, peace: list, block_name: str, offset: int) -> None:
        pygame.draw.rect(self.screen, Color.Grey,
                         (offset * 32, 5 * 32, 32 * 5, 32 * 4), 1)
        if not peace:
            return

        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j]:
                    self.screen.blit(self.get_image_for_block(Constants.VALUES[block_name]),
                                     ((j + offset) * BSIZE + Constants.BLOCK_DISPLAY_OFFSETS_X[block_name],
                                      ((i + 4) * BSIZE) + Constants.BLOCK_DISPLAY_OFFSETS_Y[block_name]))

    def draw_score(self) -> None:

        score = str(self.system.score)
        while len(score) < 9:
            score = "0" + score

        pygame.draw.rect(self.screen, Color.Grey, (BSIZE * 24,
                         BSIZE * 2, BSIZE * 5, BSIZE * 2), 1)
        self.screen.blit(self.assets.font_32.render(
            "Best", True, Color.Grey),      (BSIZE * 24 + 8, BSIZE * 2 + 2))
        self.screen.blit(self.assets.font_32.render(
            score, True, Color.LightRed),   (BSIZE * 24 + 8, BSIZE * 3))

        pygame.draw.rect(self.screen, Color.Grey, (BSIZE * 24,
                         BSIZE * 10, BSIZE * 5, BSIZE * 2), 1)
        self.screen.blit(self.assets.font_32.render(
            "Score", True, Color.Grey),     (BSIZE * 24 + 8, BSIZE * 10 + 2))
        self.screen.blit(self.assets.font_32.render(
            score, True, Color.LightGreen), (BSIZE * 24 + 8, BSIZE * 11))

    def draw_pause(self) -> None:
        if self.system.paused:
            pygame.draw.rect(self.screen, (40, 40, 40),
                             (8 * BSIZE, 250, 10 * 32, 200))
            self.screen.blit(self.text["Pause"],
                             (8 * BSIZE + 3 * 32 + 12, 310))
            self.screen.blit(self.text["Pause1"], (8 * BSIZE + 20, 360))
