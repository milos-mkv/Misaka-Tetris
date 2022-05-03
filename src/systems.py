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
        """
        Function: __init__

        Params:
            events : EventHandler   - Keep track of pressed and released keys.
            assets : Assets         - Use sounds from assets to play sounds based on actions and etc.
        """
        self.events : EventHandler = events
        self.assets : Assets       = assets

        self.reset()


    def reset(self) -> None:
        """
        Function: reset

        Brief:
            Reset all game state values. Called in constructor also initializes all fields.
        """

        # Tetris field represented as double dimensional array [20 (rows) x 10 (columns)]
        self.tetris_field   : list  = [[0 for _ in range(Constants.COLS)] for _ in range(Constants.ROWS)]

        self.move_timers    : dict  = { "down": 0,  "left": 0,  "right": 0 }        # State of move timers for moving current block on field.
        self.next_peace     : str   = random.choice(list(TETRIS_PEACES.keys()))     # Next peace in queue.
        self.ghost_cursor   : list  = [ 0, 0 ]                                      # Position of ghost cursor.
       
        self.hold_peace     : str   = None                                          # Peace in hold.
       
        self.paused         : bool  = True                                          # Pause/Resume game.
        self.pause_time     : float = 0
        self.total_time     : float = 0                                             # Total time of playing current game.

        self.level          : int   = 0                                             # Current game level. Start from 0....
        self.fall_timer     : float = 1                                            # Current block peace fall timer.
        self.cleared_lines  : int   = 0                                             # Number of cleared lines in current game.
        self.score          : int   = 0                                             # Total score.
        self.inc_level      : int   = 0                                             # Value used to determine when to level up.

        self.indices        : list  = []                                            # Indices of lines cleared, used for particles.
        self.block_ids      : list  = []                                            # Block ids in cleared indices, also used for particles.

        self.spawn_new_block()


    def spawn_new_block(self) -> None:
        """
        Function: spawn_new_block

        Brief:
            Replace current block with next block in queue and reset cursor position.
        """
        self.current_peace   : str  = self.next_peace                               # Set next peace as current peace.
        self.rotation        : int  = 0                                             # Set default rotation.
        self.cursor          : list = self.default_cursor()                         # Set default cursor.
        self.next_peace      : str  = random.choice(list(TETRIS_PEACES.keys()))     # Set random peace as next peace in queue.

        self.move_timers["down"]    = 0                                             # Reset move down timer.
        self.can_hold   = True                                                      # Enable holding peace.
        
        if self.check_for_end():                                                    # Check if new created peace spawned into exisint block.
            self.reset()                                                            # If so reset game state.


    def default_cursor(self) -> list: 
        """
        Function: default_cursor

        Brief:
            Return default cursor depending on current peace. Should be in the top middle of the field.
        """
        return [ Constants.COLS // 2 - len(self.get_current_peace()[0]) // 2, 0 ]


    def get_next_peace(self) -> list:
        """
        Function: get_next_peace

        Brief:
            Return next tetris peace with default rotation.
        """
        return TETRIS_PEACES[self.next_peace][0]


    def get_current_peace(self) -> list:
        """
        Function: get_current_peace

        Brief:
            Return current tetris peace with its current rotation.
        """
        return TETRIS_PEACES[self.current_peace][self.rotation]


    def get_hold_peace(self) -> list:
        """
        Function: get_hold_peace

        Brief:
            Return hold tetris peace with default rotation. If there is no peace in hold return None.
        """
        return None if self.hold_peace == None else TETRIS_PEACES[self.hold_peace][0]


    def check_for_end(self) -> bool:
        """
        Function: check_for_end

        Brief:
            If current peace spawns into existing peace on tetris field it should indicate end, therefore return True otherwise False.
        """
        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j] and self.tetris_field[self.cursor[Constants.Y] + i][self.cursor[Constants.X] + j]:
                    return True
        return False

    
    def update(self, delta : float) -> None:
        """
        Function: update

        Params:
            delta : float   - Elapsed time since the game function update call.

        Brief:
            Every frame update current state of the game.
        """
        if self.paused or self.pause_time > 0:
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
        """
        Function: activate_hold_peace

        Brief:
            If can swap between current and holding peace.
        """
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
        """
        Function: move_cursor_y

        Params:
            cursor : list   - Cursor. | Peace or Ghost |

        Breif:
            Move provided cursor to the lowest point on field it can go.
        """
        while not (self.check_collision_y(cursor) or (cursor[Constants.Y] + len(self.get_current_peace()) > Constants.ROWS)):
            cursor[Constants.Y] += 1


    def calc_ghost_cursor(self) -> None:
        """
        Function: cal_ghost_cursor

        Brief:
            Calculate ghost cursor position.
        """
        self.ghost_cursor = self.cursor.copy()
        self.move_cusror_y(self.ghost_cursor)


    def drop_block(self) -> None: 
        """
        Function: drop_block

        Brief:
            Hard drop current peace into current ghost position and spawn new block.
        """
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


    def move_on_y_axis(self, delta : float) -> None:
        """
        Function: move_on_y_axis

        Params:
            delta : float   - Elapsed time since the game function update call.
        
        Brief:
            Move current peace on y axis.
        """
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
        """
        Function: move_on_x_axis

        Params:
            delta : float   - Elapsed time since the game function update call.

        Brief:
            Move current peace on x axis.
        """
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
        """
        Function: check_collision_x

        Params:
            side : str      - Side on which to check collision.

        Brief:
            Check if current peace collides with blocks on x axis om provided side.
        """
        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if side == "left" and peace[i][j] and (self.cursor[Constants.X] + j - 1 < 0 or self.tetris_field[self.cursor[Constants.Y] + i][self.cursor[Constants.X] + j - 1]):
                    return True
                if side == "right" and peace[i][j] and (self.cursor[Constants.X] + j + 1 == Constants.COLS or self.tetris_field[self.cursor[Constants.Y] + i][self.cursor[Constants.X] + j + 1]):
                    return True
        return False


    def check_collision_y(self, cursor : list) -> bool:
        """
        Function: check_collision_y

        Params:
            cursor : list      - Cursor for which to check collision. | Peace or Ghost |

        Brief:
            Check if provided cursor collides with blocks on y axis om provided side.
        """
        peace = self.get_current_peace()
        for i in range(len(peace)):
            for j in range(len(peace[i])):
                if peace[i][j] and (cursor[Constants.Y] + i == Constants.ROWS or self.tetris_field[cursor[Constants.Y] + i][cursor[Constants.X] + j]):
                    return True
        return False


    def rotate_peace(self) -> None:
        """
        Function: rotate_peace

        Brief:
            Rotate current peace clockwise or counter clockwise.
        """
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
        """
        Function: check_for_cleared_lines

        Brief:
            Check for cleared lines.
        """
        for i in range(Constants.ROWS):
            if all(list(self.tetris_field[i])):
                self.block_ids.append(list(self.tetris_field[i]).copy())
                self.tetris_field[i] = [0 for _ in range(Constants.COLS)]
                self.indices.append(i)
        
        for index in self.indices:
            for i in range(index, 0, -1):
                self.tetris_field[i] = self.tetris_field[i - 1]
            self.tetris_field[0] = [0 for _ in range(Constants.COLS)]

        if len(self.indices):
            
            self.assets.channel1.play(self.assets.clear_sound)
            self.update_score(len(self.indices))
            self.inc_level += len(self.indices)
            self.update_level()
    

    def update_score(self, cleared : int) -> None:
        """
        Function: update_score

        Params:
            cleared : int   - Number of cleared lines.
        
        Brief:
            Add more value to current score. Formula for calculating score: 40 * (n + 1)   100 * (n + 1)   300 * (n + 1)   1200 * (n + 1)
        """
        self.cleared_lines += cleared
        self.score         += ((self.level + 1) * Constants.SCORES[len(self.indices) - 1])


    def update_level(self):
        """
        Function: update_level
        
        Brief:
            For every 10 cleared lines increment level.
        """
        if self.inc_level   >= 10:
            self.inc_level  -= 10
            self.level      += 1 
            self.fall_timer -= self.level * 0.01
        pass