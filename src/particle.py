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

from src.constants import Constants

class Particle(object):

    def __init__(self, position : list, velocity : list, speed : list) -> None:
        """
        Function: __init__

        Params:
            position : list    - Starting position of particle.
            velocity : list    - Rate of change of position.
            speed    : list    - Speed of particle for both x and y axis.
        """
        self.position : list    = position
        self.velocity : list    = velocity
        self.speed    : list    = speed
        self.color    : tuple   = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.size     : int     = random.randint(2, 8)


class MainMenuParticleSystem(object):

    def __init__(self) -> None:
        self.particles : list   = [ 
            Particle([random.uniform(0, Constants.SCREEN_SIZE[Constants.X]), random.uniform(0, Constants.SCREEN_SIZE[Constants.Y])],
                     [random.uniform(-0.05, 0.1), random.uniform(-0.1,  -0.2 )],
                     [random.uniform(-0.1,  0.2), random.uniform(-0.02, -0.09)]) for _ in range(120) ]


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

