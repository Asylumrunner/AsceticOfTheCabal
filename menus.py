import tcod as libtcod
import game_constants
from inspect_functions import inspect_entity

def menu(con, header, options, width, itemized=True):
    if len(options) > 26:
        raise ValueError("Too many menu options: " + len(options))

    header_height = libtcod.console_get_height_rect(con, 0, 0, width, game_constants.screen_height, header)
    body_height = libtcod.console_get_height_rect(con, 0, 0, width, game_constants.screen_height, "\n".join(options))
    height = body_height + header_height * 2

    window = libtcod.console.Console(width, height)

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = ('(' + chr(letter_index) + ') ' + option_text) if itemized else option_text
        offset = libtcod.console_print_rect_ex(window, 0, y, width, height, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += offset
        letter_index += 1
    
    libtcod.console_blit(window, 0, 0, width, height, 0, game_constants.screen_width-game_constants.character_portrait_width-width, game_constants.screen_height-height, 1.0, 0.7)

def draw_picture(con, image, width):
    picture = libtcod.console.Console(game_constants.portrait_width, game_constants.portrait_height)
    libtcod.image_blit_rect(image, picture, 0, 0, -1, -1, libtcod.BKGND_NONE)
    libtcod.console_blit(picture, 0, 0, game_constants.portrait_width, game_constants.portrait_height, con, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory):
    if len(inventory.items) == 0:
        options = ['Inventory empty']
    else:
        options = [item.name for item in inventory.items]
    
    menu(con, header, options, 44)

def dialogue_menu(con, dialogue_target):
    dialogue_target_name = dialogue_target.name
    conversation_state = dialogue_target.get_component("Character").get_conversation()
    menu(con, "<" + dialogue_target_name + ">" + "\n" + conversation_state.utterance, conversation_state.choices, 44)

def equipped_menu(con, inventory):
    listed_options = [key + ": " + (inventory.equipped[key].name if inventory.equipped[key] else "None") for key in inventory.equipped]
    menu(con, "EQUIPPED GEAR", listed_options, 44)

def inspect_menu(con, inspect_target):
    inspect_details = inspect_entity(inspect_target)
    menu(con, "INSPECTED ENTITY: {}".format(inspect_target.name), inspect_details, 44, False)
    #add a call to draw_picture here

def item_detail_menu(con, item):
    item_type = item.item.item_type.name
    description = game_constants.items[item.name]['description']
    uses = (item.item.uses + " uses") if item.item.uses != -00 else None
    listed_attributes = [item_type, description, uses]
    menu(con, item.name, listed_attributes, 44, False)

def main_menu(con, background_image):
    libtcod.image_blit_2x(background_image, con, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 5,
        libtcod.BKGND_NONE, libtcod.CENTER, "ASCETIC OF THE CABAL")
    libtcod.console_set_default_foreground(0, libtcod.red)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 4,
        libtcod.BKGND_NONE, libtcod.CENTER, "DEATH IS A GIFT TO THE PENITENT")

    menu(con, '', ['New Game', 'Continue', 'Quit'], 24)   