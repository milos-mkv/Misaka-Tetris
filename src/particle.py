"""
---------------------------------------------------------------------------------------------------------------------------------------
@file       src/particles.py
@author     Milos Milicevic (milosh.mkv@gmail.com)

@version    0.1
@date       2022-04-28
@copyright 	Copyright (c) 2022
    
Distributed under the MIT software license, see the accompanying file LICENCE or http://www.opensource.org/licenses/mit-license.php.
---------------------------------------------------------------------------------------------------------------------------------------
"""


import pygame

from random        import uniform, randint
from pygame        import Surface
from src.colors    import Color

class Particle(object):

    def __init__(self, position : list, velocity : list, speed : list, color : list, size : int) -> None:
        self.position : list  = position
        self.velocity : list  = velocity
        self.speed    : list  = speed
        self.color    : tuple = color
        self.size     : int   = size

class ParticleSystem(object):
    
    def __init__(self) -> None:
        self.particles : list = []
        
    def render(self, surface : Surface) -> None:
        for particle in self.particles:
            pygame.draw.rect(surface, particle.color, (particle.position[0], particle.position[1], particle.size, particle.size), 1)

class BackgroundParticleSystem(ParticleSystem):

    def __init__(self, width : int, height : int) -> None:
        super().__init__()
        self.width  : int = width
        self.height : int = height

        for _ in range(100):
            self.particles.append(Particle([uniform(0, width), uniform(0, height)], [uniform(-0.5, 0.5), uniform(-0.1, -0.2)],
                [uniform(-0.1,  0.1), uniform(-0.02, -0.09)], [randint(100, 255) for __ in range(3)], randint(2, 8)))
    
    def distort(self) -> None:
        for particle in self.particles:
            particle.velocity[0] += uniform(0.1, 0.5) if particle.position[0] > self.width / 2 else uniform(-0.5, -0.1)
            particle.velocity[1] -= uniform(0.1, 0.5)
    
    def boom(self) -> None:
        for particle in self.particles:
            if particle.position[1] < self.height:
                particle.velocity[0]  += uniform(3, 5) if particle.position[0] > self.width / 2  else uniform(-5, -3)
    
    def add(self, x : int, y : int) -> None:
        self.particles.append(Particle([x, y], [uniform(-0.5, 0.5), uniform(-0.1, -0.2)],
            [uniform(-0.1, 0.1), uniform(-0.02, -0.09)], [randint(100, 255) for __ in range(3)], randint(2, 8)))

    def update(self, delta : float) -> None:
        for particle in self.particles:
            particle.position[0] += particle.velocity[0] * delta * 200
            particle.velocity[0] += particle.speed[0]    * delta
            particle.position[1] += particle.velocity[1] * delta * 300
            particle.velocity[1] += particle.speed[1]    * delta

            if  particle.position[1] < 0 or particle.position[0] < 0 or particle.position[0] > self.width:
                particle.position = [randint(0, self.width), randint(self.height, self.height + 200)]
                particle.velocity = [uniform(-0.5, 0.5), uniform(-0.1 , -0.5 )]
                particle.speed    = [uniform(-0.1, 0.1), uniform(-0.02, -0.09)]
                particle.color    = [randint(100, 255) for __ in range(3)]
                particle.size     =  randint(2, 8)


class HardDropParticleSystem(ParticleSystem):

    def __init__(self) -> None:
        super().__init__()

    def add(self, x : int, y : int, offset_x : int, offset_y : int) -> None:
        self.particles.append(Particle([randint(x, offset_x), randint(y, offset_y)], [uniform(-0.01, 0.01), uniform(-1, -1)],
            [uniform(-0.1,  0.1),  uniform(-0.02, -0.09)], Color.Grey, 10))

    def update(self, delta : float) -> None:
        for particle in self.particles:
            particle.position[1] += particle.velocity[1] * delta * 200
            particle.velocity[1] += particle.speed[1]    * delta * 400

            particle.size -= delta * 15 
            if  particle.size < 1:
                self.particles.remove(particle) 