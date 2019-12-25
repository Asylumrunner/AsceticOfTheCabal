import tcod as libtcod
from game_states import GameStates

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_key(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_key(key)
    elif game_state == GameStates.INVENTORY_OPEN:
        return handle_player_inv_key(key)
    elif game_state == GameStates.MAIN_MENU:
        return handle_main_menu(key)
    elif game_state == GameStates.DIALOGUE:
        return handle_dialogue_key(key)
    return {}

def handle_player_turn_key(key):
    key_char = chr(key.c)
    if key.vk == libtcod.KEY_UP or key_char == 'k':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 'j':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'h':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'l':
        return {'move': (1, 0)}
    elif key_char == 'y':
        return {'move': (-1, -1)}
    elif key_char == 'u':
        return {'move': (1, -1)}
    elif key_char == 'b':
        return {'move': (-1, 1)}
    elif key_char == 'n':
        return {'move': (1, 1)}

    if key_char == 'g':
        return {'grab': True}
    
    if key_char == 'i':
        return {'inventory': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}
    
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    if key_char == 's':
        return {'save': True}
    
    return {}

def handle_player_dead_key(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'inventory': True}
    
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_player_inv_key(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventory_item': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

def handle_dialogue_key(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'dialogue_option': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}
    
def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'game_start': 'from_scratch'}
    elif key_char == 'b':
        return {'game_start': 'from_save'}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}
    
    return {}

    