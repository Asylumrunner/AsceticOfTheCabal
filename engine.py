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
from menus import main_menu
from game_messages import MessageLog, Message
from save import save_game, load_game
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

        # Create and initialize the Message Log
        self.message_log = MessageLog()

        #Initialize the player
        self.player = self.initialize_player()

        # Create a game map and fill it with enemies
        self.build_map()

        self.dialogue_target = None

        # Create references for the player input
        self.key = libtcod.Key()
        self.mouse = libtcod.Mouse()

        # Establish the Game State
        self.game_state = GameStates.PLAYERS_TURN
        self.previous_game_state = GameStates.PLAYERS_TURN
        self.game_running = True
        
    def initialize_player(self):
        return Entity(int(game_constants.screen_width/2), int(game_constants.screen_height/2), '@',
        libtcod.white, "Player", True, RenderOrder.ACTOR, Fighter(hp=30, defense=2, power=5), ai=None, 
        item=None, inventory=Inventory(26), message_log=self.message_log)
    
    def build_map(self, level=1):
        self.game_map = GameMap(self.message_log, level)
        self.entities = [self.player]
        self.game_map.make_map(self.player, self.entities)

        self.fov_recompute = True
        self.fov_map = initialize_fov(self.game_map)

    def grade_map_down(self):
        self.game_map.grade_down()

    def cull_dead(self):
        # Finds every entity in the game world with 0 health and kills them
        # Returns true if it kills the player, otherwise false
        player_killed = False
        dead_entities = [entity for entity in self.entities if entity.fighter and not entity.fighter.isAlive() and entity.char != '%']

        if dead_entities:
            for dead_entity in dead_entities:
                drop = dead_entity.fighter.die()
                if drop:
                    self.entities.append(drop)
                if dead_entity == self.player:
                    player_killed = True
        return player_killed

    def send_invalid_action_message(self):
        self.message_log.add_message(Message("Can't do that here"), libtcod.red)

    def start_screen(self):
        show_main_menu = True

        while show_main_menu:
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, self.key, self.mouse)
            main_menu(self.con, game_constants.main_menu_background_image)

            libtcod.console_flush()

            action = handle_keys(self.key, GameStates.MAIN_MENU)
            game_type = action.get('game_start')
            exit_game = action.get('exit')

            if exit_game:
                return False
            elif game_type == 'from_scratch':
                return True
            elif game_type == 'from_save':
                self.player, self.entities, self.game_map, self.message_log, self.game_state = load_game()
                self.fov_map = initialize_fov(self.game_map)
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
            render_all(self.con, self.panel, self.entities, self.player, self.game_map, self.fov_map, self.fov_recompute, self.message_log, self.mouse, self.game_state, self.dialogue_target)
            self.fov_recompute = False
            libtcod.console_flush()

            # Populate the game map with characters
            clear_all(self.con, self.entities)

            # Interpret the input into a game action
            action = handle_keys(self.key, self.game_state)
            move = action.get('move')
            grab = action.get('grab')
            exit = action.get('exit')
            save = action.get('save')
            gun = action.get('gun')
            inventory_item = action.get('inventory_item')
            dialogue_option = action.get('dialogue_option')
            show_inventory = action.get('inventory')
            show_equipped = action.get('equipped')
            fullscreen = action.get('fullscreen')
            go_down = action.get('go_down')
            holster = action.get('holster')

            # If players turned and it's their turn to move
            if move and self.game_state == GameStates.PLAYERS_TURN:
                # Calculate where they should move
                dx, dy = move
                destination_x = self.player.x + dx
                destination_y = self.player.y + dy

                #if not self.game_map.is_blocked(destination_x, destination_y):
                if True:
                    # If they're not about to walk into a wall, check for enemies at the destination
                    target = get_blocking_entities_at_location(self.entities, destination_x, destination_y)
                    if target and target.state == AIStates.HOSTILE:
                        # If there are enemies, attack them
                        self.player.fighter.attack(target)
                        self.game_state = GameStates.ENEMY_TURN
                    elif target and target.state == AIStates.FRIENDLY:
                        self.previous_game_state = self.game_state
                        self.dialogue_target = target
                        self.game_state = GameStates.DIALOGUE
                    else:
                        # If there are not enemies, move and mark FOV for recomputation
                        self.player.move(dx, dy)
                        self.fov_recompute = True
                        self.game_state = GameStates.ENEMY_TURN
            
            elif grab and self.game_state == GameStates.PLAYERS_TURN:
                for item in [entity for entity in self.entities if (entity.item or entity.money) and entity.x == self.player.x and entity.y == self.player.y]:
                    if item.money:
                        self.player.fighter.pick_up_money(item)
                    else:
                        self.player.inventory.add_item(item)
                    self.entities.remove(item)
                    self.game_state = GameStates.ENEMY_TURN

            elif show_inventory:
                self.previous_game_state = self.game_state
                self.game_state = GameStates.INVENTORY_OPEN
            
            elif show_equipped:
                self.previous_game_state = self.game_state
                self.game_state = GameStates.EQUIPPED_OPEN

            elif inventory_item is not None and self.previous_game_state != GameStates.PLAYER_DEAD and inventory_item < len(self.player.inventory.items):
                item_entity = self.player.inventory.items[inventory_item]
                print(item_entity.item.item_type)
                if item_entity.item.item_type != ItemType.NONE:
                    print("Equipping {}".format(item_entity.name))
                    self.player.inventory.equip_item(item_entity)
                else:
                    print("Using {}".format(item_entity.name))
                    if item_entity.item.use(self.player):
                        self.player.inventory.remove_item(item_entity)
            
            elif dialogue_option is not None:
                self.dialogue_target.character.talk(dialogue_option)

            elif go_down and self.game_state == GameStates.PLAYERS_TURN:
                if [entity for entity in self.entities if entity.x==self.player.x and entity.y==self.player.y and entity.stairs]:
                    self.build_map(entity.stairs.floor)
                    libtcod.console_clear(self.con)

            elif save:
                save_game(self.player, self.entities, self.game_map, self.message_log, self.game_state)

            elif self.game_state == GameStates.PLAYERS_TURN and gun:
                self.previous_game_state = self.game_state
                self.game_state = GameStates.PLAYER_SHOOT
                self.message_log.add_message(Message("Taking aim. Click on your target, or e to holster"))
            
            elif self.game_state == GameStates.PLAYER_SHOOT and holster:
                self.game_state = self.previous_game_state
                self.message_log.add_message(Message("Holstered your weapon"))
            
            elif self.game_state == GameStates.PLAYER_SHOOT and self.mouse.lbutton_pressed:
                target = get_shoot_target(self.mouse, self.entities, self.fov_map)
                if(target):
                    self.player.fighter.attack(target)
                    target.state = AIStates.HOSTILE
                    self.game_state = GameStates.ENEMY_TURN
                
            # Exit the game
            if exit and (self.game_state in [GameStates.INVENTORY_OPEN, GameStates.DIALOGUE, GameStates.EQUIPPED_OPEN]):
                self.game_state = self.previous_game_state
            elif exit:
                return True
            
            # Set the game to fullscreen
            if fullscreen:
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            if self.cull_dead():
                self.game_state = GameStates.PLAYER_DEAD

            if self.game_state == GameStates.ENEMY_TURN:
                for entity in self.entities:
                    if entity.ai and entity.state == AIStates.HOSTILE:
                        entity.ai.take_turn(self.player, self.fov_map, self.game_map, self.entities)
                        if self.cull_dead():
                            self.game_state = GameStates.PLAYER_DEAD

                if self.game_state != GameStates.PLAYER_DEAD:
                    self.game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    engine = Engine()
    if engine.start_screen():
        engine.main()