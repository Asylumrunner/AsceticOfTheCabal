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
from components.stairs import Stairs
import numpy as np
import game_constants
from item_generation.item_generation import generate_weapon, generate_armor

class GameMap:
    def __init__(self, message_log, dungeon_level=1):
        self.width = game_constants.map_width
        self.height = game_constants.map_height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level
        self.log = message_log

    # Intialize the map with a nested array of tiles
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    # Generates a usable game map out of rooms and the hallways connecting them
    # This algorithm will need to be refined in the future, and reworked for the city maps
    def make_map(self, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        # Essentially, this algorithm generates a random room, and checks to see if it intesects with the generated map (if it does, it breaks)
        # If not, it generates the room, and using the center of that room, connects that room with a tunnel to the previously generated room
        # if it's the first room, it plops the player in the middle of it
        # Then fill it with stuff and keep going
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

        # Once all of the rooms have been generated, plot the stairs in the middle of the last room created
        stairs_components = { "Stairs": Stairs(self.dungeon_level + 1) }
        stairs_entity = Entity(center_of_last_room_x, center_of_last_room_y, ">", libtcod.white,"Stairs Down", blocks=True, render_order=RenderOrder.ACTOR, 
                message_log=self.log, state=AIStates.INANIMATE, components=stairs_components)
        entities.append(stairs_entity)
    
    # checks to see if a given x,y coordinate is blocked
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        else:
            return False

    # carves out a "room" of the given proportions and coordinates into the map
    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    # carves a horizontal tunnel into the game map
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    # carves a vertical tunnel into the game map
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    # spawns an Entity in the map based on a name and a lookup in game_constants
    def spawn_character(self, x, y, name):
        monster_data = game_constants.npcs[name]
        monster_components = {
            "Fighter": Fighter(hp = monster_data['hp'], defense = monster_data['defense'], power = monster_data['power'], money = monster_data['money']),
            "Character": Character(description = monster_data['description'], conv_options = monster_data['conv']) if 'conv' in monster_data else None,
            "AI": BasicMonster()
        }
        return Entity(x, y, monster_data['icon'], monster_data['color'], monster_data['name'], 
                blocks=True, render_order=RenderOrder.ACTOR, message_log=self.log, state = monster_data['state'], components=monster_components)

    # Generates a random selection of NPCs and items based on the probabilities of the floor
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
                weapon_or_armor = randint(0, 1)
                if weapon_or_armor == 0:
                    entities.append(generate_weapon(floor_dict['quality_prob'], floor_dict['effect_prob'], x, y, self.log))
                else:
                    entities.append(generate_armor(floor_dict['quality_prob'], floor_dict['effect_prob'], x, y, self.log))

    # Returns the game_constants data for the current floor
    def get_floor_info(self):
        return [game_constants.floors[key] for key in game_constants.floors if self.dungeon_level in key][0]