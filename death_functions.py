import tcod as libtcod
from render_functions import RenderOrder

from game_states import GameStates

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return 'You died!', GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = '{0} is dead!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.render_order = RenderOrder.CORPSE
    monster.name = 'remains of {0}'.format(monster.name.capitalize())

    return death_message
    