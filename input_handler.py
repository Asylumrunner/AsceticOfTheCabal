import tcod as libtcod
from game_states import GameStates

# A collection of conditionals which exist to take in an input from the player (either keyboard or mouse) and extrapolate those into a game state

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
    elif game_state == GameStates.PLAYER_SHOOT:
        return handle_shoot_key(key)
    elif game_state == GameStates.EQUIPPED_OPEN:
        return handle_player_equ_key(key)
    elif game_state == GameStates.INSPECT_OPEN:
        return handle_player_insp_key(key)
    elif game_state == GameStates.SHOPPING:
        return handle_player_shop_key(key)
    return {}

def handle_player_turn_key(key):
    key_char = chr(key.c)
    if key.vk == libtcod.KEY_UP:
        return {'action': 'move', 'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN:
        return {'action': 'move', 'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT:
        return {'action': 'move', 'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT:
        return {'action': 'move', 'move': (1, 0)}
    elif key_char == 'y':
        return {'action': 'move', 'move': (-1, -1)}
    elif key_char == 'u':
        return {'action': 'move', 'move': (1, -1)}
    elif key_char == 'b':
        return {'action': 'move', 'move': (-1, 1)}
    elif key_char == 'n':
        return {'action': 'move', 'move': (1, 1)}
    elif key_char == 'e':
        return {'action': 'gun'}

    if key_char == 'g':
        return {'action': 'grab'}
    
    if key_char == 'i':
        return {'action': 'inventory'}
    elif key_char == 'p':
        return {'action': 'equipped'}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'action': 'fullscreen'}
    elif key.vk == libtcod.KEY_ENTER:
        return {'action': 'go_down'}
    
    elif key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}

    if key_char == 's':
        return {'action': 'save'}
    
    return {}

def handle_player_dead_key(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'action': 'inventory'}
    
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'action': 'fullscreen'}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}
    
    return {}

def handle_player_inv_key(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'action': 'inventory', 'inventory_item': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'action': 'fullscreen'}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}
    
    return {}

def handle_player_equ_key(key):
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'action': 'fullscreen'}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}
    
    return {}

def handle_dialogue_key(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'action': 'speak', 'dialogue_option': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'action': 'fullscreen'}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}
    
    return {}
    
def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'game_start': 'from_scratch'}
    elif key_char == 'b':
        return {'game_start': 'from_save'}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}
    
    return {}
    
def handle_shoot_key(key):
    key_char = chr(key.c)

    if key_char == 'e':
        return {'action': 'holster'}
    return {}

def handle_player_insp_key(key):
    key_char = chr(key.c)
    
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'action': 'fullscreen'}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}

    return {}

def handle_player_shop_key(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'action': 'buy', 'shop_option': index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        return {'action': 'fullscreen'}

    elif key.vk == libtcod.KEY_ESCAPE:
        return {'action': 'exit'}
    
    return {}

#TODO: Oh honey why the hell is this logic here
def get_shoot_target(mouse, entities, fov_map, fighters_only=True):
    (x, y) = (mouse.cx, mouse.cy)

    target = [entity for entity in entities if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y) and (entity.has_component("Fighter") or not fighters_only)]
    
    if(len(target) > 0):
        return target[0]
    else:
        return []