from enum import Enum

# Some misc. enums which contain the states the game can be in, as well as the AI states

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    INVENTORY_OPEN = 4
    MAIN_MENU = 5
    DIALOGUE = 6
    PLAYER_SHOOT = 7
    EQUIPPED_OPEN = 8
    INSPECT_OPEN = 9
    SHOPPING = 10
    STATUS = 11

class AIStates(Enum):
    INANIMATE = 0
    FRIENDLY = 1
    HOSTILE = 2
    