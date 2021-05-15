import tcod as libtcod
import game_constants
from inspect_functions import inspect_entity

#A set of functions designed to assist with drawing various menus (inventory, dialogue, etc)

def menu(con, title, text, options, width, selectable=True, image=None, border=None, first_option=0, con_x=10, con_y=10):
    # con = the console to blit to
    # title = always one line, the top thing on the menu
    # text = any nonselectable text that will be put between the text and options
    # options = either selectable options or just rows of data (for like a status screen)
    # width = how wide to draw the console
    # selectable = are options selectable or not
    # image = an image to draw in the corner of the menu, if there is one
    # border = the border used to draw the menu
    # first_option = this will be how I circumvent menu height issues, buy allowing the menu to render the list of options from a starting point

    # TODO: I should add in some settings to customize the color of the menu

    if border == None:
        border = game_constants.default_border

    # These functions together generate the number of lines of screen space that will be needed 
    #  to print the menu
    text_height = libtcod.console_get_height_rect(con, 0, 0, width, game_constants.screen_height, text)
    options_height = min(len(options)-first_option, 12) #this 12 should be a game constant. Eh. Also I think this needs to be retooled for long options
    height = 7 + text_height + options_height # Two rows of border, two rows of margin next to border, one row of title, one row of margin between title and text, and one row of margin between text and options

    # Then we create and set up the window with the borders
    window = libtcod.console.Console(width + 4, height) # The plus four comes from the two columns of border, plus two rows of margin
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width+4, 1, libtcod.BKGND_NONE, libtcod.LEFT, border['corner'] + (width+2) * border['top_and_bottom'] + border['corner'])
    libtcod.console_print_rect_ex(window, 0, 1, 1, height-2, libtcod.BKGND_NONE, libtcod.LEFT, border['side'] * (height-2))
    libtcod.console_print_rect_ex(window, width+3, 1, 1, height-2, libtcod.BKGND_NONE, libtcod.LEFT, border['side'] * (height-2))
    libtcod.console_print_rect_ex(window, 0, height-1, width+4, 1, libtcod.BKGND_NONE, libtcod.LEFT, border['corner'] + (width+2) * border['top_and_bottom'] + border['corner'])

    # Then we print the title and text
    libtcod.console_print_rect_ex(window, 2, 2, width, 1, libtcod.BKGND_NONE, libtcod.LEFT, title)
    libtcod.console_print_rect_ex(window, 2, 4, width, text_height, libtcod.BKGND_NONE, libtcod.LEFT, text)

    # Finally, print all options
    y = text_height + 4
    letter_index = ord('a')
    for option_text in options:
        text = ('(' + chr(letter_index) + ') ' + option_text) if selectable else option_text
        offset = libtcod.console_print_rect_ex(window, 2, y, width, height, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += offset
        letter_index += 1
    
    # Then you blit the window to console
    libtcod.console_blit(window, 0, 0, width+4, height+1, 0, con_x, con_y, 1.0, 0.7)

# Draws an image to a window. Used for character portraits in dialogue
def draw_picture(con, image, width):
    picture = libtcod.console.Console(game_constants.portrait_width, game_constants.portrait_height)
    libtcod.image_blit_rect(image, picture, 0, 0, -1, -1, libtcod.BKGND_NONE)
    libtcod.console_blit(picture, 0, 0, game_constants.portrait_width, game_constants.portrait_height, con, x, y, 1.0, 0.7)

# Creates a menu for the player's inventory
def inventory_menu(con, header, inventory):
    if len(inventory.items) == 0:
        options = ['Inventory empty']
    else:
        options = [item.name for item in inventory.items]
    
    menu(con, "Inventory Menu", "Press key to equip/use item", options, 85)

# Creates a dialogue menu for a given dialogue target
def dialogue_menu(con, dialogue_target):
    dialogue_target_name = dialogue_target.name
    conversation_state = dialogue_target.get_component("Character").get_conversation()
    menu(con, "<" + dialogue_target_name + ">", conversation_state.utterance, conversation_state.choices, 85)

# Creates a menu for the currently equipped gear of the player
def equipped_menu(con, inventory):
    listed_options = [key + ": " + (inventory.equipped[key].name if inventory.equipped[key] else "None") for key in inventory.equipped]
    menu(con, "Equipped Gear", "All gear currently equipped on the Ascetic. Press associated key to unequip", listed_options, 85)

# Creates a menu for when the player chooses to inspect an NPC or item
def inspect_menu(con, inspect_target):
    inspect_details = inspect_entity(inspect_target)
    menu(con, "Inspected Entity: {}".format(inspect_target.name), "Description should go here", inspect_details, 85, False)
    #add a call to draw_picture here

# Draws a menu for item descriptions
def item_detail_menu(con, item):
    item_type = item.item.item_type.name
    description = item['description']
    uses = (item.item.uses + " uses") if item.item.uses != -00 else None
    listed_attributes = [item_type, description, uses]
    menu(con, item.name, description, listed_attributes, 85, False)

def shopping_menu(con, shopkeeper):
    choices = ["{} (${})".format(item.name, item.get_component('Item').get_cost()) for item in shopkeeper.get_component("Shop").get_items()]
    shopkeeper_text = shopkeeper.get_component("Shop").description
    menu(con, shopkeeper.name, shopkeeper_text, choices, 85, True, None, game_constants.shop_border)

def restart_menu(con):
    menu(con, 'YOU ARE DEAD', 'CONTINUE OR PERISH', ['New Game', 'Quit'], 24, True, border=game_constants.death_border)

# Draws the main menu of the game on boot
def main_menu(con, background_image):
    libtcod.image_blit_2x(background_image, con, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 5,
        libtcod.BKGND_NONE, libtcod.CENTER, "ASCETIC OF THE CABAL")
    libtcod.console_set_default_foreground(0, libtcod.red)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 4,
        libtcod.BKGND_NONE, libtcod.CENTER, "DEATH IS A GIFT TO THE PENITENT")

    menu(con, 'CHOOSE YOUR FATE', '', ['New Game', 'Continue', 'Quit'], 24, True, con_x=40, con_y=50) 