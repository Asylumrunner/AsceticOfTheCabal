from enum import Enum

class GameStates(Enum):
    PLAYERS_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    INVENTORY_OPEN = 4
    MAIN_MENU = 5
    