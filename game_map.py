import tcod as libtcod
from entity import Entity
from tile import Tile
from rect import Rect
from random import randint
from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from components.character import Character
from render_functions import RenderOrder
from game_states import AIStates
from stairs import Stairs
import numpy as np
import item_functions
import game_constants

class GameMap:
    def __init__(self, message_log, dungeon_level=1):
        self.width = game_constants.map_width
        self.height = game_constants.map_height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level
        self.log = message_log

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(game_constants.max_rooms):
            w = randint(game_constants.room_min_size, game_constants.room_max_size)
            h = randint(game_constants.room_min_size, game_constants.room_max_size)    

            x = randint(0, game_constants.map_width - w - 1)
            y = randint(0, game_constants.map_height - h - 1)
            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()
                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                    print("Placing player at {}, {}".format(player.x, player.y))
                    libtcod.mouse_move(player.x, player.y)
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                self.place_entities(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1

        stairs = Stairs(self.dungeon_level + 1)
        stairs_entity = Entity(center_of_last_room_x, center_of_last_room_y, ">", libtcod.white,"Stairs Down", blocks=True, render_order=RenderOrder.ACTOR, 
                fighter=None, ai=None, character=None, item=None, inventory=None, message_log=self.log, state=AIStates.INANIMATE, stairs=stairs)
        entities.append(stairs_entity)
    
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        else:
            return False

    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
        
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def spawn_character(self, x, y, name):
        monster_data = game_constants.npcs[name]
        fighter_component = Fighter(hp = monster_data['hp'], defense = monster_data['defense'], power = monster_data['power'], money = monster_data['money'])
        character_component = Character(description = monster_data['description'], conv_options = monster_data['conv']) if 'conv' in monster_data else None
        ai_component = BasicMonster()
        return Entity(x, y, monster_data['icon'], monster_data['color'], monster_data['name'], 
                blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component, character = character_component, item=None, inventory=None, message_log=self.log, state = monster_data['state'], stairs=None)

    def spawn_item(self, x, y, name):
        item_data = game_constants.items[name]
        item_funcs = [item_functions.item_fuction_dict[function] for function in item_data['functions']]
        return Entity(x, y, item_data['icon'], item_data['color'], item_data['name'], blocks=False, render_order=RenderOrder.ITEM, fighter=None, ai=None, item=Item(item_funcs, item_data['uses'], item_data['type'], **item_data['kwargs']), inventory=None, message_log=self.log, stairs=None)

    def place_entities(self, room, entities):
        number_of_monsters = randint(0, game_constants.max_monsters_per_room)
        floor_dict = self.get_floor_info()

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                entities.append(self.spawn_character(x, y, np.random.choice(floor_dict['enemies']['names'], 1, floor_dict['enemies']['distribution'])[0]))
        
        number_of_items = randint(0, game_constants.max_items_per_room)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 + 1, room.y2 -1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                entities.append(self.spawn_item(x, y, "Cool Hat"))

    def get_floor_info(self):
        return [game_constants.floors[key] for key in game_constants.floors if self.dungeon_level in key][0]