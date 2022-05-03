

from pygame import Surface
import pygame

from src.assets import Assets
from src.systems import GameplaySystem
from src.constants import Constants
from src.colors import Color
from src.particle import MainMenuParticleSystem

import random
from src.states import GlobalStates

class Particle(object):

    def __init__(self, block_id : int, x : int, y : int) -> None:
        self.block_id : int  = block_id
        self.position : list = [ x, y ]
        self.velocity : list = [ random.uniform(-0.5, 0.5), random.uniform(-0.1, -0.5) ]
        self.speed    : int  = [ random.uniform(-0.1, 0.1), random.uniform( 0.1,  0.5) ]

    def update(self, delta : float) -> None:
        self.position[0] += self.velocity[0]
        self.velocity[0] += (self.speed[0] * delta)
        
        self.position[1] += self.velocity[1]
        self.velocity[1] += (self.speed[1] * delta * 20)

            

class ParticleSystem(object):

    def __init__(self) -> None:
        self.particles : list = []

    def update(self, delta : float) -> None:
        for particle in self.particles:
            particle.update(delta)
            if particle.position[Constants.Y] > Constants.SCREEN_SIZE[1]:
                self.particles.remove(particle)


class Effect(object):

    def __init__(self, x, y) -> None:
        self.index = 0
        self.position = (x, y)

class Renderer(object):     

    def __init__(self, screen : Surface, assets : Assets, system : GameplaySystem) -> None:

        self.screen : Surface        = screen
        self.assets : Assets         = assets
        self.system : GameplaySystem = system
        
        self.drop_effects : list = []

        self.particle_system : ParticleSystem = ParticleSystem()
        self.mmp = MainMenuParticleSystem()
        self.init_text()


    def init_text(self) -> None:
        """
        Initialize all text that can be prerendered in game.
        """
        self.text : dict = {
            "Hold":  self.assets.font.render("Hold",  True, Color.White),
            "Next":  self.assets.font.render("Next",  True, Color.White),
            "Score": self.assets.font.render("Score", True, Color.White),
            "Level": self.assets.font.render("Level", True, Color.White),
            "Lines": self.assets.font.render("Lines", True, Color.White),
            ":":     self.assets.font.render(":",     True, Color.White),
            "Play":  self.assets.font.render("Play",  True, Color.White),
            "Time":  self.assets.font.render("Time :",  True, Color.White),
            "Pause": self.assets.font_48.render("Pause", True, Color.White),
            "Pause1": self.assets.font.render("Press [P] to unpause", True, Color.White),
        }


    def get_image_for_block(self, peace : int) -> Surface:
        """
        Return specifed block peace image.
        """
        return self.assets.block_images[ peace - 2 ]


    def render(self, delta : float) -> None:
        self.screen.fill(Color.Black)

        if  self.system.pause_time > 0:
            self.system.pause_time -=delta

        if len(self.system.indices) > 0:
            while len(self.system.indices):
                h_offset = self.system.indices.pop()
                b_list   = self.system.block_ids.pop()

                i = 1
                for id in b_list:
                    self.particle_system.particles.append(Particle(id, (8 + i) * Constants.BLOCK_SIZE, h_offset * Constants.BLOCK_SIZE))
                    i += 1
                    
            self.system.indices = []
            self.system.pause_time = 0.3

            for p in self.mmp.particles:
                p.speed[1] -= 2
        self.mmp.update(delta)
        for particle in self.mmp.particles:
            pygame.draw.rect(self.screen, particle.color, (particle.position[0], particle.position[1], particle.size, particle.size), 1)
        
        self.draw_tetris_field(offset=8)
        self.particle_system.update(delta)
        for p in self.particle_system.particles:
            self.screen.blit(self.assets.block_images[p.block_id - 2], tuple(p.position))
        self.draw_next_block()
        self.draw_hold_block()
        self.draw_info_board()
        self.draw_time()
        self.draw_pause()


        self.screen.blit(self.assets.misaka_image, (600, 0) )


        


    def draw_tetris_field(self, offset : int) -> None:

        for i in range(Constants.ROWS):
            for j in range(Constants.COLS):
                if self.system.tetris_field[i][j]:
                    self.screen.blit(self.get_image_for_block(self.system.tetris_field[i][j]), ((j + offset) * Constants.BLOCK_SIZE , (i + 1) * Constants.BLOCK_SIZE - Constants.BLOCK_SIZE))

        peace = self.system.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j] == 1  and self.system.pause_time <= 0:
                    self.screen.blit(self.get_image_for_block(Constants.VALUES[self.system.current_peace]), (
                        (self.system.cursor[Constants.X] + j + offset) * Constants.BLOCK_SIZE,
                        (self.system.cursor[Constants.Y] + i + 1 )     * Constants.BLOCK_SIZE - Constants.BLOCK_SIZE)) 
                    self.screen.blit(self.assets.block_images[7], (
                        (self.system.ghost_cursor[Constants.X] + j + offset) * Constants.BLOCK_SIZE,
                        (self.system.ghost_cursor[Constants.Y] + i)          * Constants.BLOCK_SIZE - Constants.BLOCK_SIZE))

        self.screen.blit(self.assets.background_image, (0, 0) )
        self.screen.blit(
        self.assets.logo_image,( Constants.BLOCK_SIZE , Constants.BLOCK_SIZE ))


    def draw_info_board(self) -> None:

        self.screen.blit(self.text["Level"], ( 40, 225 + 130 ))
        self.screen.blit(self.text[":"], ( 127, 225 + 130 ))
        self.screen.blit(self.assets.font.render(str(self.system.level), True, Color.LightRed), (140, 225 + 130))

        self.screen.blit(self.text["Lines"], ( 40, 255 + 130 ))
        self.screen.blit(self.text[":"], ( 127, 255 + 130 ))
        self.screen.blit(self.assets.font.render(str(self.system.cleared_lines), True, Color.LightRed), (140, 255 + 130))

        score = str(self.system.score)
        while len(score) < 9: 
            score = "0" + score

        self.screen.blit(self.text["Score"], ( Constants.BLOCK_SIZE * 20 + 8, Constants.BLOCK_SIZE ))
        self.screen.blit(self.assets.font.render(score, True, Color.LightGreen), (Constants.BLOCK_SIZE * 20 +8, Constants.BLOCK_SIZE * 2))


    def draw_next_block(self) -> None:
        self.draw_block(self.system.get_next_peace(), self.system.next_peace, 20)
        self.screen.blit(self.text["Next"], (Constants.BLOCK_SIZE * 20 + 4, Constants.BLOCK_SIZE * 5))

    def draw_hold_block(self) -> None:
        self.draw_block(self.system.get_hold_peace(), self.system.hold_peace, 1 )
        self.screen.blit(self.text["Hold"], (Constants.BLOCK_SIZE + 4, Constants.BLOCK_SIZE * 5))

    def draw_block(self, peace : list, block_name : str, offset : int) -> None:
        if not peace: 
            return

        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j]:
                    self.screen.blit(self.get_image_for_block(Constants.VALUES[block_name]), 
                        ((j + offset) * Constants.BLOCK_SIZE + Constants.BLOCK_DISPLAY_OFFSETS_X[block_name], 
                        ((i + 4) * Constants.BLOCK_SIZE) + Constants.BLOCK_DISPLAY_OFFSETS_Y[block_name]))

    def draw_time(self) -> None:
        self.screen.blit(self.text["Time"], ( 40, 225 + 257 ))
        self.screen.blit(self.assets.font.render("{}:{}".format(int(self.system.total_time // 60),int( self.system.total_time % 60)), 
        True, Color.LightBlue), ( 122, 225 + 257 ))

    def draw_pause(self) -> None:
        if self.system.paused:
            pygame.draw.rect(self.screen, (40, 40, 40), (8 * Constants.BLOCK_SIZE, 250, 10 * 32, 200))
            self.screen.blit(self.text["Pause"], ( 8 * Constants.BLOCK_SIZE + 3 * 32 + 12, 310 ))
            self.screen.blit(self.text["Pause1"], ( 8 * Constants.BLOCK_SIZE + 20, 360 ))