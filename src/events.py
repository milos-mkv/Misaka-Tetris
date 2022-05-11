import pygame

from src.states   import GlobalStates
from pygame.event import Event

class EventHandler(object):

    def __init__(self) -> None:
        self.keys : dict  = { "down": False, "left": False, "right": False, "up": False, "z": False, "space": False, "c": False, "p": False,
                              "enter": False }

    def key(self, k : str) -> None:
        if self.keys[k]:
            self.keys[k] = False
            return True
        return False

    def handle_key_events(self, event : Event, down : bool) -> None:
        if event.key == pygame.K_DOWN:  self.keys["down"]   = down
        if event.key == pygame.K_LEFT:  self.keys["left"]   = down; GlobalStates.FIRST_MOVE[0] = down 
        if event.key == pygame.K_RIGHT: self.keys["right"]  = down; GlobalStates.FIRST_MOVE[1] = down 
        if event.key == pygame.K_UP:    self.keys["up"]     = down
        if event.key == pygame.K_SPACE: self.keys["space"]  = down 
        if event.key == pygame.K_z:     self.keys["z"]      = down
        if event.key == pygame.K_c:     self.keys["c"]      = down
        if event.key == pygame.K_p:     self.keys["p"]      = down
        if event.key == pygame.K_RETURN:self.keys["enter"]  = down