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

import random
import pygame
from src.colors    import Color
from pygame        import Surface
from src.constants import Constants

class Particle(object):

    def __init__(self, position : list, velocity : list, speed : list) -> None:
        self.position : list    = position
        self.velocity : list    = velocity
        self.speed    : list    = speed
        self.color    : tuple   = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.size     : int     = random.randint(2, 8)


class BackgroundParticleSystem(object):

    def __init__(self) -> None:
        self.particles : list   = [ 
            Particle([random.uniform(0, Constants.SCREEN_SIZE[Constants.X]), random.uniform(0, Constants.SCREEN_SIZE[Constants.Y])],
                     [random.uniform(-0.05, 0.1), random.uniform(-0.1,  -0.2 )],
                     [random.uniform(-0.1,  0.2), random.uniform(-0.02, -0.09)]) for _ in range(100) ]


    def update(self, delta : float) -> None:
        for particle in self.particles:
            self.update_particle(particle, delta)
            if  particle.position[Constants.Y] < 0:
                particle.position = [random.uniform(0, Constants.SCREEN_SIZE[Constants.X]), Constants.SCREEN_SIZE[Constants.Y]]
                particle.velocity = [random.uniform(-0.5, 0.5), random.uniform(-0.1, -0.5)]


    def update_particle(self, particle : Particle, delta : float) -> None:
        for i in range(2):
            particle.position[i] += particle.velocity[i]
            particle.velocity[i] += particle.speed[i] * delta

    def render(self, screen : Surface) -> None:
        for particle in self.particles:
            pygame.draw.rect(screen, particle.color, (particle.position[0], particle.position[1], particle.size, particle.size), 1)



class HardDropParticles(object):

    def __init__(self) -> None:
        self.particles : list = []

    def add(self, position : list) -> None:
        self.particles.append(Particle(position,  [random.uniform(-0.01, 0.01), random.uniform(-0.1, -0.2)], [random.uniform(-0.1,  0.1), random.uniform(-0.02, -0.09)] ))

    def update(self, delta : float) -> None:
        for particle in self.particles:
            particle.size -= delta
            self.update_particle(particle, delta)
            if  particle.size < 1:
                self.particles.remove(particle)

    def update_particle(self, particle : Particle, delta : float) -> None:
        particle.position[0] += particle.speed[0] * delta * 200
        particle.position[1] += -100 * delta
            # particle.velocity[i] += 

    def render(self, screen : Surface) -> None:
        for particle in self.particles:
            pygame.draw.rect(screen, Color.White, (particle.position[0], particle.position[1], 20, 20)) #particle.size, particle.size))

