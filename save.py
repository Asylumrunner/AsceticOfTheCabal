import shelve
import os

def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open('savegame', 'n') as savegame:
        savegame['player_index'] = entities.index(player)
        savegame['entities'] = entities
        savegame['map'] = game_map
        savegame['message_log'] = message_log
        savegame['state'] = game_state

def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError
    
    with shelve.open('savegame', 'r') as savegame:
        entities = savegame['entities']
        player = entities[savegame['player_index']]
        game_map = savegame['map']
        message_log = savegame['message_log']
        game_state = savegame['state']

        return player, entities, game_map, message_log, game_state