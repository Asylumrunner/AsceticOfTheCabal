from enum import Enum

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    INVENTORY_OPEN = 4
    MAIN_MENU = 5
    DIALOGUE = 6

class AIStates(Enum):
    INANIMATE = 0
    FRIENDLY = 1
    HOSTILE = 2
    