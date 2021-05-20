import tcod as libtcod

from entity import Entity, get_blocking_entities_at_location
from input_handler import handle_keys, get_shoot_target
from render_functions import render_all, clear_all, RenderOrder
from game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates, AIStates
from components.item import ItemType
from components.inventory import Inventory
from components.fighter import Fighter
from components.devotee import Devotee
from components.status_container import StatusContainer
from menus import main_menu
from game_messages import MessageLog, Message
from save import save_game, load_game
from aiming_functions import draw_line
from item_generation.item_generation import generate_starting_pistol
import game_constants

#TODO: Update comments

class Engine():
    def __init__(self):
        # Set up the game window
        #libtcod.console_set_custom_font('spritesheet.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_set_custom_font('Winterwing_Curses.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        libtcod.console_init_root(game_constants.screen_width, game_constants.screen_height, 'Ascetic of the Cabal', True, libtcod.RENDERER_SDL2, vsync=True)

        # Establish the primary console as well as the detail panel
        self.con = libtcod.console.Console(game_constants.screen_width, game_constants.screen_height)
        self.panel = libtcod.console.Console(game_constants.screen_width, game_constants.panel_height)

        # Create references for the player input
        self.key = libtcod.Key()
        self.mouse = libtcod.Mouse()

        self.initialize_game()

    # Initializes a lot of run-specific items. Kept outside of init because it has to be re-run on a restart
    def initialize_game(self):
        # Create and initialize the Message Log
        self.message_log = MessageLog()

        #Initialize the player
        self.player = self.initialize_player()

        # Create a game map and fill it with enemies
        self.build_map()

        self.player_target = None

        # Establish the Game State
        self.game_state = GameStates.PLAYERS_TURN
        self.previous_game_state = GameStates.PLAYERS_TURN
        self.game_running = True
        
    # Creates the player object, with all associated defaults
    # This can and probably should be moved to another file
    def initialize_player(self):
        player_components = {
            "Fighter": Fighter(hp=300, defense=2, power=5),
            "Inventory": Inventory(26),
            "Devotee": Devotee(100),
            "StatusContainer": StatusContainer()
        }

        player = Entity(int(game_constants.screen_width/2), int(game_constants.screen_height/2), '@',
        libtcod.white, "Ascetic", True, RenderOrder.ACTOR, message_log=self.message_log, state=AIStates.INANIMATE, components=player_components)

        player.get_component("Inventory").equip_item(generate_starting_pistol(self.message_log))
        return player
    
    # Generates a game map and initializes the FOV map of it
    def build_map(self, level=1):
        self.game_map = GameMap(self.message_log, level)
        self.entities = [self.player]
        self.game_map.make_map(self.player, self.entities)

        self.fov_recompute = True
        self.fov_map = initialize_fov(self.game_map)

    # Literally 0 recollection what this does
    def grade_map_down(self):
        self.game_map.grade_down()

    def cull_dead(self):
        # Finds every entity in the game world with 0 or less health and kills them
        # Returns true if it kills the player, otherwise false
        player_killed = False
        dead_entities = [entity for entity in self.entities if entity.has_component("Fighter") and not entity.get_component("Fighter").isAlive() and entity.char != '%']

        if dead_entities:
            for dead_entity in dead_entities:
                drop = dead_entity.get_component("Fighter").die()
                if drop:
                    self.entities.append(drop)
                if dead_entity == self.player:
                    player_killed = True
        return player_killed

    def send_invalid_action_message(self):
        self.message_log.add_message(Message("Can't do that here"), libtcod.red)

    # Initializes the game's start menu, and captures any player input on that menu and passes it to the appropriate handler
    def start_screen(self):
        show_main_menu = True

        while show_main_menu:
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.key, self.mouse)
            main_menu(self.con, game_constants.main_menu_background_image)

            libtcod.console_flush()

            action = handle_keys(self.key, GameStates.MAIN_MENU)
            game_type = action.get('game_start')
            exit_game = action.get('action') == 'exit'

            if exit_game:
                return False
            elif game_type == 'from_scratch':
                return True
            elif game_type == 'from_save':
                self.player, self.entities, self.game_map, self.message_log, self.game_state = load_game()
                self.fov_map = initialize_fov(self.game_map)

                for entity in self.entities:
                    if entity.get_log() != self.message_log:
                        entity.log = self.message_log
                        
                return True

    def main(self):
        # Game Loop
        while self.game_running:
            # Check input streams for an event
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.key, self.mouse)

            # If we need to recompute fov, do so
            if self.fov_recompute:
                recompute_fov(self.fov_map, self.player.x, self.player.y)
            
            # Render the game world according to current FOV, mark FOV recompute as complete, and flush to console
            render_all(self.con, self.panel, self.entities, self.player, self.game_map, self.fov_map, self.fov_recompute, self.message_log, self.mouse, self.game_state, self.player_target)
            self.fov_recompute = False
            libtcod.console_flush()

            # Populate the game map with characters
            clear_all(self.con, self.entities)

            # Interpret the input into a game action
            input = handle_keys(self.key, self.game_state)
            action = input.get('action')

            inventory_item = input.get('inventory_item') if 'inventory_item' in input else None
            dialogue_option = input.get('dialogue_option') if 'dialogue_option' in input else None
            shop_option = input.get('shop_option') if 'shop_option' in input else None
            unequip_item = input.get('slot') if 'slot' in input else None

            # If players turned and it's their turn to move
            if action == 'move' and self.game_state == GameStates.PLAYERS_TURN:
                # Calculate where they should move
                dx, dy = input.get('move')
                destination_x = self.player.x + dx
                destination_y = self.player.y + dy

                #if not self.game_map.is_blocked(destination_x, destination_y):
                if True:
                    # If they're not about to walk into a wall, check for enemies at the destination
                    target = get_blocking_entities_at_location(self.entities, destination_x, destination_y)
                    if target and target.state == AIStates.HOSTILE:
                        # If there are enemies, attack them
                        self.player.get_component("Fighter").attack(target)
                        self.game_state = GameStates.ENEMY_TURN
                    elif target and target.state == AIStates.FRIENDLY:
                        self.previous_game_state = self.game_state
                        self.player_target = target
                        self.game_state = GameStates.DIALOGUE
                    else:
                        # If there are not enemies, move and mark FOV for recomputation
                        self.player.move(dx, dy)
                        self.fov_recompute = True
                        self.game_state = GameStates.ENEMY_TURN
            
            # If the player grabs something, check if there is an object at their feet, and either have them pick it up (if it's an Item) or add it to their wallet (if it's money)
            elif action == 'grab' and self.game_state == GameStates.PLAYERS_TURN:
                for item in [entity for entity in self.entities if (entity.has_component("Item") or entity.has_component("Money")) and entity.x == self.player.x and entity.y == self.player.y]:
                    if item.has_component("Money"):
                        self.player.get_component("Fighter").pick_up_money(item)
                    else:
                        self.player.get_component("Inventory").add_item(item)
                    self.entities.remove(item)
                    self.game_state = GameStates.ENEMY_TURN

            # Open up the inventory menu
            elif action == 'inventory' and inventory_item is None:
                self.previous_game_state = self.game_state
                self.game_state = GameStates.INVENTORY_OPEN
            
            # Open up the equipped menu
            elif action == 'equipped':
                self.previous_game_state = self.game_state
                self.game_state = GameStates.EQUIPPED_OPEN

            elif action == 'unequip' and self.game_state == GameStates.EQUIPPED_OPEN:
                self.player.get_component("Inventory").unequip_slot(unequip_item)

            # if the player has selected an inventory item to use, get the item object, and equip it if it's vgear, or use it if it's a consumable (like a potion) 
            elif inventory_item is not None and self.previous_game_state != GameStates.PLAYER_DEAD and inventory_item < len(self.player.get_component("Inventory").items):
                item_entity = self.player.get_component("Inventory").items[inventory_item]
                if item_entity.get_component("Item").item_type != ItemType.NONE:
                    self.player.get_component("Inventory").equip_item(item_entity)
                else:
                    if item_entity.get_component("Item").use(self.player):
                        self.player.get_component("Inventory").remove_item(item_entity)
            
            # if the player is in dialogue, provide the dialogue option to the target's Character object
            elif dialogue_option is not None:
                dialogue_response = self.player_target.get_component("Character").talk(dialogue_option)
                if dialogue_response.shop:
                    self.game_state = GameStates.SHOPPING

            # if the player attempts to go down some stairs, make sure they're on stairs, then build a new map and clear the console
            elif action == 'go_down' and self.game_state == GameStates.PLAYERS_TURN:
                stairs_candidates = [entity for entity in self.entities if entity.x==self.player.x and entity.y==self.player.y and entity.has_component("Stairs")]
                if stairs_candidates:
                    self.build_map(stairs_candidates[0].get_component("Stairs").floor)
                    libtcod.console_clear(self.con)
            
            # Save the game
            elif action == 'save':
                save_game(self.player, self.entities, self.game_map, self.message_log, self.game_state)

            # if the player draws their gun, change to a player shoot state and await gunfire
            elif self.game_state == GameStates.PLAYERS_TURN and action == 'gun':
                if(self.player.get_component("Inventory").slot_filled("RANGED")):
                    self.previous_game_state = self.game_state
                    self.game_state = GameStates.PLAYER_SHOOT
                    self.message_log.add_message(Message("Taking aim. Click on your target, or e to holster"))
                else:
                    self.message_log.add_message(Message("No ranged weapon equipped!"))
            
            # if the player already has their gun drawn and presses the draw button, holster it instead
            elif self.game_state == GameStates.PLAYER_SHOOT and action == 'holster':
                self.game_state = self.previous_game_state
                self.message_log.add_message(Message("Holstered your weapon"))
            
            # if the player has their gun drawn and clicks on a target, check if there is line of sight
            # and if so, shoot the target. This sets the AI to hostile if it isn't already (this should be handled by Fighter)
            elif self.game_state == GameStates.PLAYER_SHOOT and self.mouse.lbutton_pressed:
                target = get_shoot_target(self.mouse, self.entities, self.fov_map)
                if(target):
                    line_of_sight = draw_line((self.player.x, self.player.y), (target.x, target.y))
                    if not [space for space in line_of_sight if self.game_map.is_blocked(space[0], space[1])]:
                        self.player.get_component("Fighter").ranged_attack(target)
                        target.state = AIStates.HOSTILE
                        self.game_state = GameStates.ENEMY_TURN
                    else:
                        self.message_log.add_message(Message("You don't have a clear line of sight!"))
            
            # if the player right clicks something, get open up the inspect menu for that target
            elif self.mouse.rbutton_pressed and self.game_state != GameStates.INSPECT_OPEN:
                target = get_shoot_target(self.mouse, self.entities, self.fov_map, False)
                if(target):
                    self.player_target = target
                    self.previous_game_state = self.game_state
                    self.game_state = GameStates.INSPECT_OPEN
            
            # If the player is buying something, they make the purchase
            elif action == 'buy' and shop_option is not None:
                target.get_component("Shop").purchase(shop_option, self.player)

            elif action == 'status':
                self.previous_game_state = self.game_state
                self.game_state = GameStates.STATUS
                
            # Exit the game
            if action == 'exit' and (self.game_state in [GameStates.INVENTORY_OPEN, GameStates.DIALOGUE, GameStates.EQUIPPED_OPEN, GameStates.SHOPPING, GameStates.INSPECT_OPEN, GameStates.STATUS]):
                self.game_state = self.previous_game_state
            elif action == 'exit':
                return True
            
            # Set the game to fullscreen
            if action == 'fullscreen':
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            # cull_dead returns true if the player is dead, so this conditional calls it to cull the dead, and then
            # checks if the game is over
            if self.cull_dead():
                self.game_state = GameStates.PLAYER_DEAD

            # when it's the AI's turn, find every entity that has AI and move it (if it's hostile)
            if self.game_state == GameStates.ENEMY_TURN:
                for entity in self.entities:
                    if entity.has_component("AI") and entity.state == AIStates.HOSTILE:
                        entity.get_component("AI").take_turn(self.player, self.fov_map, self.game_map, self.entities)
                        if self.cull_dead():
                            self.game_state = GameStates.PLAYER_DEAD

                if self.game_state != GameStates.PLAYER_DEAD:
                    self.game_state = GameStates.PLAYERS_TURN

            # TODO: need a check somewhere around here to tick condition clocks, and then to apply conditions

            if action == 'restart':
                libtcod.console_clear(self.con)
                self.initialize_game()

if __name__ == '__main__':
    engine = Engine()
    if engine.start_screen():
        engine.main()