import pygame
from src.states import GlobalStates
from pygame.event import Event

class EventHandler(object):

    def __init__(self) -> None:
        self.keys : dict  = { "down": False, "left": False, "right": False, "up": False, "z": False, "space": False, "c": False, "p": False,
                              "enter": False }
        self.joysticks : list = [ pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count()) ]
        print(self.joysticks)
        # self.joystick_buttons : dict [ "1": False, "2": False, "3": False, "4": False, "start": False, "select": False,
        # "top": False, "right": False, "down": False, ""]


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

    def handle_joystick_buttons(self, event : Event) -> None:

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0: self.keys["space"] = True
            if event.button == 1: self.keys["c"]     = True
            if event.button == 2: self.keys["up"]    = True
            if event.button == 3: self.keys["z"]     = True

        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0: self.keys["space"] = False
            if event.button == 1: self.keys["c"]     = False
            if event.button == 2: self.keys["up"]    = False
            if event.button == 3: self.keys["z"]     = False

        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0 and round(event.value) == 1:
                self.keys["right"] = True
            if event.axis == 0 and round(event.value) == -1:
                self.keys["left"] = True
            if event.axis == 1 and round(event.value) == 1:
                self.keys["down"] = True

            if event.axis == 0 and round(event.value) == 0:
                self.keys["right"] = False
            if event.axis == 0 and round(event.value) == 0:
                self.keys["left"] = False
            if event.axis == 1 and round(event.value) == 0:
                self.keys["down"] = False

            print(event.value)
            