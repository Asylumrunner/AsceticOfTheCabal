import tcod as libtcod
from entity import Entity
from tile import Tile
from rect import Rect
from random import randint
from components.ai import ai_dictionary
from components.fighter import Fighter
from components.item import Item
from components.character import Character
from components.shop import Shop
from components.status_container import StatusContainer
from render_functions import RenderOrder
from game_states import AIStates
from components.stairs import Stairs
import numpy as np
import game_constants
from item_generation.item_generation import generate_weapon, generate_armor, generate_potion
from utilities.csv_reader import read_csv_to_dict
import time
import random
from math import floor

class GameMap:
    def __init__(self, message_log, dungeon_level=1):
        self.width = game_constants.map_width
        self.height = game_constants.map_height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level
        self.log = message_log
        self.floor_dict = self.get_floor_info()

        all_rooms = read_csv_to_dict("./data/rooms.csv")
        self.room_options = {key: data for (key, data) in all_rooms.items() if int(data['min_floor']) <= self.dungeon_level and int(data['max_floor']) >= self.dungeon_level}

    # Intialize the map with a nested array of tiles
    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    # Generates a usable game map out of rooms and the hallways connecting them
    # This algorithm will need to be refined in the future, and reworked for the city maps
    def make_map(self, player, entities):
        start_time = time.time()
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
                    libtcod.mouse_move(player.x, player.y)
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                self.populate_room(new_room, entities)
                rooms.append(new_room)
                num_rooms += 1

        # Once all of the rooms have been generated, plot the stairs in the middle of the last room created
        stairs_components = { "Stairs": Stairs(self.dungeon_level + 1) }
        stairs_entity = Entity(center_of_last_room_x, center_of_last_room_y, ">", libtcod.white,"Stairs Down", blocks=True, render_order=RenderOrder.ACTOR, 
                message_log=self.log, state=AIStates.INANIMATE, components=stairs_components)
        self.tiles[center_of_last_room_x][center_of_last_room_y].add_entity(stairs_entity)
        entities.insert_entity(stairs_entity)
        self.compute_dijkstra_map([stairs_entity], "stairs")

        print("Map generated in {} seconds".format(time.time() - start_time))
    
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
            "Fighter": Fighter(hp = monster_data['hp'], defense = monster_data['defense'], power = monster_data['power'], money = monster_data['money'], abilities=monster_data['abilities']),
            "Character": Character(monster_data['description'], monster_data['conv']) if 'conv' in monster_data else None,
            "AI": ai_dictionary[monster_data['ai']](),
            "Shop": Shop(game_constants.shops[monster_data['shop']], monster_data['shop_description'], self.log) if 'shop' in monster_data else None,
            "StatusContainer": StatusContainer()
        }
        return Entity(x, y, monster_data['icon'], monster_data['color'], monster_data['name'], 
                blocks=True, render_order=RenderOrder.ACTOR, message_log=self.log, state = monster_data['state'], components=monster_components)

    # Generates a random selection of NPCs and items based on the probabilities of the floor
    def place_entities(self, room, entities):
        self.populate_room(room, entities)
        number_of_monsters = randint(0, game_constants.max_monsters_per_room)
        

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                entities.insert_entity(self.spawn_character(x, y, np.random.choice(self.floor_dict['enemies']['names'], 1, self.floor_dict['enemies']['distribution'])[0]))
        
        number_of_items = randint(0, game_constants.max_items_per_room)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 + 1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                weapon_or_armor = randint(0, 1)
                if weapon_or_armor == 0:
                    entities.insert_entity(generate_weapon(self.floor_dict['quality_prob'], self.floor_dict['effect_prob'], x, y, self.log))
                else:
                    entities.insert_entity(generate_armor(self.floor_dict['quality_prob'], self.floor_dict['effect_prob'], x, y, self.log))

    def populate_room(self, room, entities):
        room_to_select = self.room_options[random.choice(list(self.room_options))]
        
        for i in range(int(room_to_select['minor_enemies'])):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                entities.insert_entity(self.spawn_character(x, y, np.random.choice(self.floor_dict['minor_enemies']['names'], 1, self.floor_dict['minor_enemies']['distribution'])[0]))


        for i in range(int(room_to_select['med_enemies'])):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                entities.insert_entity(self.spawn_character(x, y, np.random.choice(self.floor_dict['med_enemies']['names'], 1, self.floor_dict['med_enemies']['distribution'])[0]))


        for i in range(int(room_to_select['major_enemies'])):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                entities.insert_entity(self.spawn_character(x, y, np.random.choice(self.floor_dict['major_enemies']['names'], 1, self.floor_dict['major_enemies']['distribution'])[0]))


        for i in range(int(room_to_select['shopkeeper'])):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                entities.insert_entity(self.spawn_character(x, y, np.random.choice(self.floor_dict['shopkeeper']['names'], 1, self.floor_dict['shopkeeper']['distribution'])[0]))

        for i in range(int(room_to_select['neutrals'])):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                entities.insert_entity(self.spawn_character(x, y, np.random.choice(self.floor_dict['neutrals']['names'], 1, self.floor_dict['neutrals']['distribution'])[0]))

        for i in range(int(room_to_select['item_spawn'])):
            x = randint(room.x1 + 1, room.x2 -1)
            y = randint(room.y1 +1, room.y2 -1)

            if not any(entities.get_sublist(lambda entity: entity.x == x and entity.y == y)):
                weapon_or_armor = randint(0, 2)
                if weapon_or_armor == 0:
                    weapon = generate_weapon(self.floor_dict['quality_prob'], self.floor_dict['effect_prob'], x, y, self.log)
                    entities.insert_entity(weapon)
                elif weapon_or_armor == 1:
                    armor = generate_armor(self.floor_dict['quality_prob'], self.floor_dict['effect_prob'], x, y, self.log)
                    entities.insert_entity(armor)
                else:
                    entities.insert_entity(generate_potion(x, y, self.log))
            

    # Returns the game_constants data for the current floor
    def get_floor_info(self):
        return [game_constants.floors[key] for key in game_constants.floors if self.dungeon_level in key][0]

    # Upates a map tile with the location of a new entity
    def add_entity_to_map(self, entity, x, y):
        self.tiles[x][y].add_entity(entity)

    # Removes an entity from the given map tile
    def remove_entity_from_map(self, entity, x, y):
        self.tiles[x][y].remove_entity(entity)

    # Updates the map's record of where a given entity is
    def move_entity_on_map(self, entity, old_x, old_y, new_x, new_y):
        self.tiles[old_x][old_y].remove_entity(entity)
        self.tiles[new_x][new_y].add_entity(entity)

    # Iterates through the map computing dijkstra map values for the purpose of rapid pathfinding
    def compute_dijkstra_map(self, goals, name, flee=False):
        start_time = time.time()

        self.reset_dijkstra_map_values(name)

        tiles_to_check = set([(goal.x, goal.y) for goal in goals])
        weight = -1
        while tiles_to_check:
            weight += 1
            default_neighbors_found = set()
            for coord in tiles_to_check:
                self.tiles[coord[0]][coord[1]].set_dijkstra_map_value(name, weight)
                if coord[0] > 0 and self.tiles[coord[0]-1][coord[1]].get_dijkstra_map_value(name) == 0:
                    default_neighbors_found.add((coord[0]-1, coord[1]))
                if coord[0] < self.width and self.tiles[coord[0]+1][coord[1]].get_dijkstra_map_value(name) == 0:
                    default_neighbors_found.add((coord[0]+1, coord[1]))
                if coord[1] > 0 and self.tiles[coord[0]][coord[1]-1].get_dijkstra_map_value(name) == 0:
                    default_neighbors_found.add((coord[0], coord[1]-1))
                if coord[1] < self.height and self.tiles[coord[0]][coord[1]+1].get_dijkstra_map_value(name) == 0:
                    default_neighbors_found.add((coord[0], coord[1]+1))
            if not default_neighbors_found:
                maximum_points = tiles_to_check
            tiles_to_check = default_neighbors_found
        
        for entity in goals:
            self.tiles[entity.x][entity.y].set_dijkstra_map_value(name, 0)

        print("Dijkstra maps generated in {} seconds for {}".format(time.time() - start_time, name))

        # If flee is set to true, then once we generate the map, we immediately generate another Dijkstra map
        # using an inverted method, which will generate a map that can be used to intelligently _flee_ the goals
        start_time = time.time()
        if flee:
            for row in self.tiles:
                for tile in row:
                    tile.set_dijkstra_map_value(name+'_flee', floor(tile.get_dijkstra_map_value(name) * -1.2))

            checked = []
            for x in range(self.width):
                checked.append([])
                for y in range(self.height):
                    checked[x].append(False)
            print("Min points found in {}".format(time.time() - start_time))
            
            tiles_to_check = set(maximum_points)
            weight = floor(weight * -1.2)
            while tiles_to_check:
                weight += 1
                default_neighbors_found = set()
                for coord in tiles_to_check:
                    checked[coord[0]][coord[1]] = True
                    if self.tiles[coord[0]][coord[1]].get_dijkstra_map_value(name+'_flee') > weight:
                        self.tiles[coord[0]][coord[1]].set_dijkstra_map_value(name+'_flee', weight)
                    if coord[0] > 0 and not self.tiles[coord[0]-1][coord[1]].blocked and not checked[coord[0]-1][coord[1]]:
                        default_neighbors_found.add((coord[0]-1, coord[1]))
                    if coord[0] < self.width and not self.tiles[coord[0]+1][coord[1]].blocked and not checked[coord[0]+1][coord[1]]:
                        default_neighbors_found.add((coord[0]+1, coord[1]))
                    if coord[1] > 0 and not self.tiles[coord[0]][coord[1]-1].blocked and not checked[coord[0]][coord[1]-1]:
                        default_neighbors_found.add((coord[0], coord[1]-1))
                    if coord[1] < self.height and not self.tiles[coord[0]][coord[1]+1].blocked and not checked[coord[0]][coord[1]+1]:
                        default_neighbors_found.add((coord[0], coord[1]+1))
                tiles_to_check = default_neighbors_found
    
        print("Flee maps generated in {} seconds".format(time.time() - start_time))
 
    def reset_dijkstra_map_values(self, name):
        for column in self.tiles:
            for tile in column:
                if tile.blocked :
                    tile.set_dijkstra_map_value(name, -1)
                else:
                    tile.set_dijkstra_map_value(name, 0)
    
    def get_tile(self, x, y):
        return self.tiles[x][y]
    
    def get_adjacent_tiles(self, x, y):
        adjacent_tiles = []
        adjacent_tiles.append(self.tiles[x][y-1] if y > 0 else None)
        adjacent_tiles.append(self.tiles[x+1][y] if x < self.wifth else None)
        adjacent_tiles.append(self.tiles[x][y+1] if y < self.height else None)
        adjacent_tiles.append(self.tiles[x-1][y] if x > 0 else None)
        return adjacent_tiles