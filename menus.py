import tcod as libtcod
import game_constants

def menu(con, header, options, width):
    if len(options) > 26:
        raise ValueError("Too many menu options: " + len(options))

    header_height = libtcod.console_get_height_rect(con, 0, 0, width, game_constants.screen_height, header)
    height = len(options) + header_height

    window = libtcod.console.Console(width, height)

    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1
    
    x = int(game_constants.screen_width / 2 - width / 2)
    y = int(game_constants.screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory):
    if len(inventory.items) == 0:
        options = ['Inventory empty']
    else:
        options = [item.name for item in inventory.items]
    
    menu(con, header, options, game_constants.inventory_width)

def dialogue_menu(con, dialogue_target):
    conversation_state = dialogue_target.character.get_conversation()
    menu(con, conversation_state.utterance, conversation_state.choices, 36)

def main_menu(con, background_image):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 5,
        libtcod.BKGND_NONE, libtcod.CENTER, "ASCETIC OF THE CABAL")
    libtcod.console_set_default_foreground(0, libtcod.red)
    libtcod.console_print_ex(0, int(game_constants.screen_width/2), int(game_constants.screen_height/2) - 4,
        libtcod.BKGND_NONE, libtcod.CENTER, "DEATH IS A GIFT TO THE PENITENT")

    menu(con, '', ['New Game', 'Continue', 'Quit'], 24)   