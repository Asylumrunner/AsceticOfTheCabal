import tcod as libtcod
import game_constants
from inspect_functions import inspect_entity

#A set of functions designed to assist with drawing various menus (inventory, dialogue, etc)

def new_menu(con, title, text, options, width, selectable=True, image=None, border=None, first_option=0):
    # con = the console to blit to
    # title = always one line, the top thing on the menu
    # text = any nonselectable text that will be put between the text and options
    # options = either selectable options or just rows of data (for like a status screen)
    # width = how wide to draw the console
    # selectable = are options selectable or not
    # image = an image to draw in the corner of the menu, if there is one
    # border = the border used to draw the menu
    # first_option = this will be how I circumvent menu height issues, buy allowing the menu to render the list of options from a starting point

    # These functions together generate the number of lines of screen space that will be needed 
    #  to print the menu
    text_height = libtcod.console_get_height_rect(con, 0, 0, width, game_constants.screen_height, text)
    options_height = min(len(options)-first_option, 12) #this 12 should be a game constant. Eh. Also I think this needs to be retooled for long options
    height = 7 + text_height + options_height # Two rows of border, two rows of margin next to border, one row of title, one row of margin between title and text, and one row of margin between text and options

    # Then we create and set up the window with the borders
    window = libtcod.console.Console(width + 4, height) # The plus four comes from the two columns of border, plus two rows of margin
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width+4, 1, border['corner'] + (width+2) * border['top_and_bottom'] + border['corner'])
    libtcod.console_print_rect_ex(window, 1, 0, 1, height-2, border['side'] * (height-2))
    libtcod.console_print_rect_ext(window, 1, width, 1, height-2, border['side'] * (height-2))
    libtcod.console_print_rect_ex(window, 0, height, width+4, 1, border['corner'] + (width+2) * border['top_and_bottom'] + border['corner'])

    

def menu(con, header, options, width, itemized=True):
    #hard-wiring in a maximimal list length of 26 items
    if len(options) > 26:
        raise ValueError("Too many menu options: " + len(options))

    # These functions together generate the number of lines of screen space that will be needed 
    #  to print the menu
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, game_constants.screen_height, header)
    body_height = libtcod.console_get_height_rect(con, 0, 0, width, game_constants.screen_height, "\n".join(options))
    height = body_height + header_height * 2

    # Then, a window of the needed proportions is drawn, its foreground drawn and a window printed
    window = libtcod.console.Console(width, height)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # Then, the header is drawn and menu options are drawn with letter indexes added to them (if itemized is true)
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = ('(' + chr(letter_index) + ') ' + option_text) if itemized else option_text
        offset = libtcod.console_print_rect_ex(window, 0, y, width, height, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += offset
        letter_index += 1
    
    # Then you blit the window to console
    libtcod.console_blit(window, 0, 0, width, height, 0, game_constants.screen_width-game_constants.character_portrait_width-width, game_constants.screen_height-height, 1.0, 0.7)

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
    
    menu(con, header, options, 44)

# Creates a dialogue menu for a given dialogue target
def dialogue_menu(con, dialogue_target):
    dialogue_target_name = dialogue_target.name
    conversation_state = dialogue_target.get_component("Character").get_conversation()
    menu(con, "<" + dialogue_target_name + ">" + "\n" + conversation_state.utterance, conversation_state.choices, 44)

# Creates a menu for the currently equipped gear of the player
def equipped_menu(con, inventory):
    listed_options = [key + ": " + (inventory.equipped[key].name if inventory.equipped[key] else "None") for key in inventory.equipped]
    menu(con, "EQUIPPED GEAR", listed_options, 44)

# Creates a menu for when the player chooses to inspect an NPC or item
def inspect_menu(con, inspect_target):
    inspect_details = inspect_entity(inspect_target)
    menu(con, "INSPECTED ENTITY: {}".format(inspect_target.name), inspect_details, 44, False)
    #add a call to draw_picture here

# Draws a menu for item descriptions
def item_detail_menu(con, item):
    item_type = item.item.item_type.name
    description = game_constants.items[item.name]['description']
    uses = (item.item.uses + " uses") if item.item.uses != -00 else None
    listed_attributes = [item_type, description, uses]
    menu(con, item.name, listed_attributes, 44, False)

# Draws the main menu of the game on boot
def main_menu(con, background_image):
    libtcod.image_blit_2x(background_image, con, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 5,
        libtcod.BKGND_NONE, libtcod.CENTER, "ASCETIC OF THE CABAL")
    libtcod.console_set_default_foreground(0, libtcod.red)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 4,
        libtcod.BKGND_NONE, libtcod.CENTER, "DEATH IS A GIFT TO THE PENITENT")

    menu(con, '', ['New Game', 'Continue', 'Quit'], 24)   