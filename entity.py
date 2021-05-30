import math
import tcod as libtcod
from game_states import AIStates
from render_functions import RenderOrder

# The single catch-all prototype class for everything that has a presence of any kind on screen in the game world
class Entity:
    
    def __init__(self, x, y, char, color, name, blocks=False, render_order = RenderOrder.CORPSE, message_log=None, state=AIStates.INANIMATE, components={}):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.log = message_log
        self.state = state
        self.components = components

        # There are so many kinds of components that can be slapped onto an entity
        # that a generic components dict just handles all of them without much concern for
        # what specific components exist
        for key in self.components:
            if self.components[key]:
                self.components[key].owner = self

        # Names of entities can be changed by various effects. This serves as a constant record of an entity's name should it be changed
        self.base_name = name

    def get_log(self):
        return self.log

    def get_components(self):
        return self.components
    
    # returns true if a given component is present
    def has_component(self, component_name):
        return component_name in self.components and self.components[component_name] != None
    
    # returns the specific component object if it exists
    def get_component(self, component_name):
        return self.components[component_name] if component_name in self.components else None
        
    # moves the entity a certain number of spaces (actually moving on the game map will be handled when the map re-renders)
    def move(self, x, y):
        self.x += x
        self.y += y
    
    #moves the entity towards the target
    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Random movement algorithms might accidentally call this using the entity's exact location
        # Break out early with that to avoid a divide by 0 error
        if distance == 0:
            return

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or entities.get_sublist(lambda entity: entity.x == self.x+dx and entity.y == self.y+dy and entity.blocks)):
            self.move(dx, dy)
    
    # checks the distance towards a target
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    # an implementation of astar movement for an entity. This feels like it shouldn't be here TBH
    def move_astar(self, target, entities, game_map):
        fov_map = libtcod.map.Map(game_map.width, game_map.height)

        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov_map, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)
            
        for entity in entities.get_entity_set():
            if entity.blocks and entity != self and entity != target:
                libtcod.map_set_properties(fov_map, entity.x, entity.y, True, False)
        
        my_path = libtcod.path_new_using_map(fov_map, 1.41)

        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y
        
        else:
            self.move_towards(target.x, target.y, game_map, entities)
        
        libtcod.path_delete(my_path)

