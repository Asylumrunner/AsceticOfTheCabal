import tcod as libtcod

from entity import Entity, get_blocking_entities_at_location
from input_handler import handle_keys
from render_functions import render_all, clear_all, RenderOrder
from game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from components.fighter import Fighter
from game_messages import MessageLog
import game_constants
    
def initialize_player(message_log):
    return Entity(int(game_constants.screen_width/2), int(game_constants.screen_height/2), '@',
     libtcod.white, "Player", True, RenderOrder.ACTOR, Fighter(hp=30, defense=2, power=5), None, message_log)

def main():

    # Set up the game window
    libtcod.console_set_custom_font('spritesheet.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(game_constants.screen_width, game_constants.screen_height, 'Ascetic of the Cabal', False, libtcod.RENDERER_SDL2, vsync=True)

    # Establish the primary console as well as the detail panel
    con = libtcod.console.Console(game_constants.screen_width, game_constants.screen_height)
    panel = libtcod.console.Console(game_constants.screen_width, game_constants.panel_height)

    # Create and initialize the Message Log
    message_log = MessageLog()

    # Create a game map and fill it with enemies
    game_map = GameMap(message_log)
    player = initialize_player(message_log)
    entities = [player]
    game_map.make_map(player, entities)

    # Initialize the FOV
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Create references for the player input
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Establish the Game State
    game_state = GameStates.PLAYERS_TURN
    game_running = True

    # Game Loop
    while game_running:
        # Check input streams for an event
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        # If we need to recompute fov, do so
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y)
        
        # Render the game world according to current FOV, mark FOV recompute as complete, and flush to console
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, mouse)
        fov_recompute = False
        libtcod.console_flush()

        # Populate the game map with characters
        clear_all(con, entities)

        # Interpret the input into a game action
        action = handle_keys(key)
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        # If players turned and it's their turn to move
        if move and game_state == GameStates.PLAYERS_TURN:
            # Calculate where they should move
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                # If they're not about to walk into a wall, check for enemies at the destination
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    # If there are enemies, attack them
                    player.fighter.attack(target)
                else:
                    # If there are not enemies, move and mark FOV for recomputation
                    player.move(dx, dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN
            
        # Exit the game
        if exit:
            return True
        
        # Set the game to fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        dead_entities = [entity for entity in entities if not entity.fighter.isAlive() and entity.char != '%']

        if dead_entities:
            for dead_entity in dead_entities:
                dead_entity.fighter.die()
                if dead_entity == player:
                    game_state = GameStates.PLAYER_DEAD

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    entity.ai.take_turn(player, fov_map, game_map, entities)
                    dead_entities = [entity for entity in entities if not entity.fighter.isAlive() and entity.char != '%']
                    if dead_entities:
                        for dead_entity in dead_entities:
                            dead_entity.fighter.die()
                            if dead_entity == player:
                                game_state = GameStates.PLAYER_DEAD
            if game_state != GameStates.PLAYER_DEAD:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    main()