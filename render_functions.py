import tcod as libtcod
from enum import Enum
from game_states import GameStates
from menus import inventory_menu, dialogue_menu, equipped_menu, inspect_menu
import game_constants

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

# returns a list of capitalized names of anything under the mouse's current position
def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

# Renders a bar (like a health or mana bar) that is proportionately filled based on some value versus a maximum
def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    
    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)
    
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))

    
# Renders everything onto the game screen. Probably the single most complicated function in the game atm
def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, mouse, game_state, target):

    # The good news is, we can reuse and skip recalculations for a lot of shit if the fov doesn't need to be recalculated
    if fov_recompute:
        # Collect color info for the various tiles based on the floor
        colors = game_map.get_floor_info()['colors']
        for y in range(game_map.height):
            for x in range(game_map.width):
                #iterating through every tile in the map, we check to see if it's visible, and if it's an empty space or a wall
                visible = fov_map.fov[y][x]
                wall = game_map.tiles[x][y].block_sight

                #if it's visible, we draw either a wall or the ground, based on which it is
                if visible:
                    if wall:
                        libtcod.console_set_default_foreground(con, colors['light_wall'])
                        libtcod.console_put_char(con, x, y, libtcod.CHAR_BLOCK3, libtcod.BKGND_NONE)
                    else:
                        libtcod.console_set_default_foreground(con, colors['light_ground'])
                        libtcod.console_put_char(con, x, y, libtcod.CHAR_BLOCK1, libtcod.BKGND_NONE)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    #if it is not visible, but the player has previously been there, we draw a darker version of the sprite instead
                    if wall:
                        libtcod.console_set_default_foreground(con, colors['dark_wall'])
                        libtcod.console_put_char(con, x, y, libtcod.CHAR_BLOCK3, libtcod.BKGND_NONE)
                    else:
                        libtcod.console_set_default_foreground(con, colors['dark_ground'])
                        libtcod.console_put_char(con, x, y, libtcod.CHAR_BLOCK1, libtcod.BKGND_NONE)
    
    #We then sort every entity by render order. Entities later in the render order will appear on top of things earlier
    entities_in_render_order = sorted(entities, key= lambda x: x.render_order.value)

    #then, we draw every entity on the map
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map, fov_map)

    # Now, we wipe the panel (that is, the bar beneath the main view)
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # We then print every message in the message log to the panel
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    # This goddamn mess renders the constant UI elements, currently bound to the bottom left of the screen
    render_bar(panel, 1, 1, game_constants.bar_width, 'HP', player.get_component("Fighter").hp, player.get_component("Fighter").max_hp, libtcod.light_red, libtcod.darker_red)
    libtcod.console_set_default_foreground(panel, libtcod.green)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT, "${}".format(player.get_component("Fighter").money))
    libtcod.console_set_default_foreground(panel, libtcod.lighter_blue)
    render_bar(panel, 1, 2, game_constants.bar_width, 'DEVOTION', player.get_component("Devotee").curr_devotion, player.get_component("Devotee").max_devotion, libtcod.light_blue, libtcod.darker_blue)
    libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT, "Level {}".format(game_map.dungeon_level))
    #libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT, "({}, {})".format(player.x, player.y))
    #libtcod.console_print_ex(panel, 1, 6, libtcod.BKGND_NONE, libtcod.LEFT, "({}, {})".format(mouse.cx, mouse.cy))
    libtcod.console_print_ex(panel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,' '.join(player.get_component("StatusContainer").get_statuses()))

    # This bit prints out a list of everything currently under the mouse
    libtcod.console_set_default_foreground(panel, libtcod.light_grey)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))
    
    # Now that the main console and the panel are done, blit them onto the screen
    libtcod.console_blit(con, 0, 0, game_constants.screen_width, game_constants.screen_height, 0, 0, 0)
    libtcod.console_blit(panel, 0, 0, game_constants.screen_width, game_constants.panel_height, 0, 0, game_constants.panel_y)

    # Depending on various game states, draw a menu onto the screen
    if game_state == GameStates.INVENTORY_OPEN:
        inventory_menu(con, "Press the indicated key to use item", player.get_component("Inventory"))
    elif game_state == GameStates.DIALOGUE and target:
        #character_portrait(target)
        dialogue_menu(con, target)
    elif game_state == GameStates.EQUIPPED_OPEN:
        equipped_menu(con, player.get_component("Inventory"))
    elif game_state == GameStates.INSPECT_OPEN:
        inspect_menu(con, target)

# Removes every entity in the game from the screen
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

# Draws a character portrait. This... needs some work
def character_portrait(target):
    portrait_image = libtcod.image_load('green.png')
    libtcod.image_blit_rect(portrait_image, 0, game_constants.screen_width-game_constants.character_portrait_width, game_constants.panel_y, game_constants.character_portrait_width, game_constants.panel_height, libtcod.BKGND_SET)

# Draws an entity onto the screen, using the entity information to determine icon and color
def draw_entity(con, entity, game_map, fov_map):
    if fov_map.fov[entity.y][entity.x] or (entity.has_component("Stairs") and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

# CLears an individual entity from the console
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)

