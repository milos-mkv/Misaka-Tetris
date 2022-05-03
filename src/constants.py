
class Constants:
    SCREEN_SIZE             : tuple = (1150, 700)
    BLOCK_SIZE              : int   = 32
    ROWS                    : int   = 21
    COLS                    : int   = 10
    X                       : int   = 0
    Y                       : int   = 1
    MAX_FPS                 : int   = 120
    DAS                     : float = 0.1
    MOVE_DIR                : dict  = { "left": -1, "right": 1 }
    BLOCK_DISPLAY_OFFSETS_X : dict  = { "T": 32, "L": 32, "J": 32, "O": 48, "I": 16, "S": 32, "Z": 32 }
    BLOCK_DISPLAY_OFFSETS_Y : dict  = { "T": 64, "L": 32, "J": 64, "O": 64, "I": 48, "S": 32, "Z": 32 }
    VALUES                  : dict  = { "T": 2,  "L": 3,  "J": 4,  "O": 5,  "I": 6,  "S": 7,  "Z": 8  }
    SCORES                  : list  = [ 40, 100, 300, 1200 ]
