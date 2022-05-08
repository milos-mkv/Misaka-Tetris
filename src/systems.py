"""
@file       src/systems.py
@author     Milos Milicevic (milosh.mkv@gmail.com)

@version    0.1
@date       2022-04-28
@copyright 	Copyright (c) 2022
    
Distributed under the MIT software license, see the accompanying file LICENCE or http://www.opensource.org/licenses/mit-license.php.
"""

import random

from src.peaces     import TETRIS_PEACES
from src.assets     import Assets
from src.constants  import Constants
from src.events     import EventHandler
from src.states     import GlobalStates


class GameplaySystem(object):

    def __init__(self, events : EventHandler, assets : Assets) -> None:
        self.events : EventHandler = events
        self.assets : Assets       = assets

        self.reset()


    def reset(self) -> None:
        self.tetris_field   : list  = [[0 for _ in range(Constants.COLS)] for _ in range(Constants.ROWS)]

        self.move_timers    : dict  = { "down": 0,  "left": 0,  "right": 0 }
        self.next_peace     : str   = random.choice(list(TETRIS_PEACES.keys())) 
        self.ghost_cursor   : list  = [ 0, 0 ] 
       
        self.hold_peace     : str   = None 
       
        self.paused         : bool  = False
        self.pause_time     : float = 0
        self.total_time     : float = 0

        self.level          : int   = 0
        self.fall_timer     : float = 1
        self.cleared_lines  : int   = 0        
        self.score          : int   = 0 
        self.inc_level      : int   = 0  


        self.clear_time     : bool  = False

        self.indices        : list  = []
        self.block_ids      : list  = [] 

        self.dropped_hard   : bool  = False
        self.dropped_hard_cursor = []

        self.spawn_new_block()


    def is_dropped_hard(self) -> bool:
        if self.dropped_hard:
            self.dropped_hard = False
            return True
        return False

    def spawn_new_block(self) -> None:
        self.current_peace   : str  = self.next_peace
        self.rotation        : int  = 0  
        self.cursor          : list = self.default_cursor()  
        self.next_peace      : str  = random.choice(list(TETRIS_PEACES.keys()))  

        self.move_timers["down"]    = 0   
        self.can_hold   = True   
        
        if self.check_for_end():  
            self.reset()   


    def default_cursor(self) -> list: 
        return [ Constants.COLS // 2 - len(self.get_current_peace()[0]) // 2, 0 ]


    def get_next_peace(self) -> list:
        return TETRIS_PEACES[self.next_peace][0]


    def get_current_peace(self) -> list:
        return TETRIS_PEACES[self.current_peace][self.rotation]


    def get_hold_peace(self) -> list:
        return None if self.hold_peace == None else TETRIS_PEACES[self.hold_peace][0]


    def check_for_end(self) -> bool:
        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j] and self.tetris_field[self.cursor[Constants.Y] + i][self.cursor[Constants.X] + j]:
                    return True
        return False

    
    def update(self, delta : float) -> None:
        if self.paused or self.clear_time:
            return

        self.total_time += delta

        self.activate_hold_peace()                  # Step 1: Check if hold peace is activated.
        self.calc_ghost_cursor()                    # Step 2: Update ghost cursor.
        self.drop_block()                           # Step 3: Check if hard drop was used.
        self.move_on_x_axis(delta)                  # Step 4: Check for movement on x axis.
        self.move_on_y_axis(delta)                  # Step 5: Check for movement on y axis.
        self.rotate_peace()                         # Step 6: Check for rotation.
        self.check_for_cleared_lines()              # Step 7: Check if there is a match.


    def activate_hold_peace(self) -> None:
        if not self.events.keys["c"] or not self.can_hold:
            return

        self.events.keys["c"] = False 
        self.current_peace, self.hold_peace = self.hold_peace, self.current_peace
            
        if self.current_peace:  self.cursor = self.default_cursor()
        else:                   self.spawn_new_block()

        if self.check_for_end():
            self.current_peace, self.hold_peace = self.hold_peace, self.current_peace
            return

        self.rotation = 0
        self.can_hold = False

    
    def move_cusror_y(self, cursor : list):
        while not (self.check_collision_y(cursor) or (cursor[Constants.Y] + len(self.get_current_peace()) > Constants.ROWS)):
            cursor[Constants.Y] += 1


    def calc_ghost_cursor(self) -> None:
        self.ghost_cursor = self.cursor.copy()
        self.move_cusror_y(self.ghost_cursor)


    def drop_block(self) -> None: 
        if not self.events.keys["space"]:
            return
        
        self.events.keys["space"] = False
        

        self.move_cusror_y(self.cursor)

        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j]:
                    self.tetris_field[self.cursor[Constants.Y] + i - 1][self.cursor[Constants.X] + j] = Constants.VALUES[self.current_peace]
        
        self.spawn_new_block()
        self.assets.channel1.play(self.assets.drop_sound)
        self.dropped_hard = True
        self.dropped_hard_cursor = self.ghost_cursor.copy()


    def move_on_y_axis(self, delta : float) -> None:
        self.move_timers["down"] += delta
        if not (self.move_timers["down"] >= self.fall_timer or (self.events.keys["down"] and self.move_timers["down"] >= 0.04)):
            return

        self.move_timers["down"]  = 0
        self.cursor[Constants.Y] += 1

        if not (self.check_collision_y(self.cursor) or (self.cursor[Constants.Y] + len(self.get_current_peace()) > Constants.ROWS)):
            return

        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j]:
                    self.tetris_field[self.cursor[Constants.Y] + i - 1][self.cursor[Constants.X] + j] = Constants.VALUES[self.current_peace]

        self.spawn_new_block()
        self.assets.channel1.play(self.assets.drop_sound)


    def move_on_x_axis(self, delta : float) -> None:
        if not self.events.keys["left"] and not self.events.keys["right"]:
            return

        side = "left" if self.events.keys["left"] else "right"
        self.move_timers[side] += delta

        #
        # TODO: FIX MOVE TIMERS
        #
        if not (GlobalStates.FIRST_MOVE[side == "right"] or self.move_timers[side] > Constants.DAS):
            return

        GlobalStates.FIRST_MOVE[side == "right"] = False
        if not self.check_collision_x(side):
            self.cursor[Constants.X] += Constants.MOVE_DIR[side]

        self.move_timers[side] = 0


    def check_collision_x(self, side : str) -> bool:
        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if side == "left" and peace[i][j] and (self.cursor[Constants.X] + j - 1 < 0 or self.tetris_field[self.cursor[Constants.Y] + i][self.cursor[Constants.X] + j - 1]):
                    return True
                if side == "right" and peace[i][j] and (self.cursor[Constants.X] + j + 1 == Constants.COLS or self.tetris_field[self.cursor[Constants.Y] + i][self.cursor[Constants.X] + j + 1]):
                    return True
        return False


    def check_collision_y(self, cursor : list) -> bool:
        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j] and (cursor[Constants.Y] + i == Constants.ROWS or self.tetris_field[cursor[Constants.Y] + i][cursor[Constants.X] + j]):
                    return True
        return False


    def rotate_peace(self) -> None:
        if not self.events.keys["up"] and not self.events.keys["z"]:
            return

        if self.events.keys["up"]: side = True ; self.events.keys["up"] = False
        if self.events.keys["z" ]: side = False; self.events.keys["z" ] = False

        old_rotation = self.rotation
        
        if side: self.rotation = 0 if self.rotation + 1 > 3 else self.rotation + 1 # Rotate clockwise
        else:    self.rotation = 3 if self.rotation - 1 < 0 else self.rotation - 1 # Rotate counter clockwise

        peace = self.get_current_peace()

        if self.cursor[Constants.Y] + len(peace) > Constants.ROWS:
            self.rotation = old_rotation
            return

        old_x = self.cursor[Constants.X]

        if (self.cursor[Constants.X] < 0):                              self.cursor[Constants.X] = 0
        elif self.cursor[Constants.X] + len(peace[0]) > Constants.COLS: self.cursor[Constants.X] = Constants.COLS - len(peace[0]) 

        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if self.tetris_field[self.cursor[Constants.Y] + i][self.cursor[Constants.X] + j] and peace[i][j]:
                    self.rotation            = old_rotation
                    self.cursor[Constants.X] = old_x
                    return


    def check_for_cleared_lines(self) -> None:
        if self.clear_time:
            return

        for i in range(Constants.ROWS):
            if all(list(self.tetris_field[i])):
                self.indices.append(i)
        
        if len(self.indices):
            self.clear_time = True
            self.assets.channel1.play(self.assets.clear_sound)
            self.update_score(len(self.indices))
            self.update_level()


    def clear(self) -> None:
        self.clear_time = False
                    
        for index in self.indices:
            for i in range(index, 0, -1):
                self.tetris_field[i] = self.tetris_field[i - 1]
                self.tetris_field[0] = [0 for _ in range(Constants.COLS)]
        
        self.indices = []

    def update_score(self, cleared : int) -> None:
        self.cleared_lines += cleared
        self.score         += ((self.level + 1) * Constants.SCORES[len(self.indices) - 1])


    def update_level(self):
        self.inc_level += len(self.indices)
        if self.inc_level   >= 10:
            self.inc_level  -= 10
            self.level      += 1 
            self.fall_timer -= self.level * 0.01
        