import tcod as libtcod
from random import randint
from enum import Enum

# A hold-all file for the various NPC behaviors, all of which are encapsulated within their own class
# Each behavior implements take_turn, describing what it should do when its turn comes around

# All player and non-player characters have a Faction, which is used to map the relationships between
# entities on the game map. This will determine who attacks who, who comes to whose aid, etc
class Factions(Enum):
    LONER = 0
    PLAYER = 1
    HERETICS = 2
    CITIZENS = 3
    MONSTERS = 4
    DIVINE = 5
    WILD_ANIMALS = 6

class BasicMonster:
    def __init__(self, allies=[], enemies=[]):
        self.allies = allies
        self.enemies = enemies

    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        
        #if the monster is in view, move towards the player using A*. If the player is in range, attack them
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.get_component("Fighter").hp > 0:
                monster.get_component("Fighter").attack(target)
        
        #TODO: Monsters can't make ranged attacks, need to determine a monster's range and implement that

class Coward:
    def __init__(self, allies=[], enemies=[]):
        self.allies = allies
        self.enemies = enemies

    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                toughest_friend = self.find_toughest_friend(target, entities)
                if monster.distance_to(toughest_friend) >= 2:
                    monster.move_astar(toughest_friend, entities, game_map)
            elif target.get_component("Fighter").hp > 0:
                monster.get_component("Fighter").attack(target)

    def find_toughest_friend(self, target, entities):
        toughest_friend = None
        max_toughness = -1

        for entity in [entity for entity in entities if entity.has_component("Fighter") and entity != target and entity != self.owner]:
            entity_toughness = entity.get_component("Fighter").hp + (2 * entity.get_component("Fighter").power)
            if entity_toughness > max_toughness or (entity_toughness == max_toughness and self.owner.distance_to(toughest_friend) > self.owner.distance_to(entity)):
                toughest_friend = entity
                max_toughness = entity_toughness
        
        return toughest_friend

class Scavenger:
    def __init__(self, allies=[], enemies=[]):
        self.corpse = None
        self.allies = allies
        self.enemies = enemies
    
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner

        if not self.corpse:
            corpse = self.find_nearest_corpse(entities)
            if self.corpse:
                print("CORPSE SELECTED: {}".format(corpse.name))

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2 and target.get_component("Fighter").get_health_percentage() < 0.5:
                monster.move_astar(target, entities, game_map)
            elif monster.distance_to(target) < 2 and target.get_component("Fighter").get_health_percentage() < 0.5:
                monster.get_component("Fighter").attack(target)
            elif self.corpse and monster.distance_to(self.corpse) >= 2:
                monster.move_astar(self.corpse, entities, game_map)
            else:
                x = monster.x + randint(-1, 1)
                y = monster.y + randint(-1, 1)
                monster.move_towards(x, y, game_map, entities)
        elif self.corpse and monster.distance_to(self.corpse) >= 2:
            monster.move_astar(self.corpse, entities, game_map)
    
    def find_nearest_corpse(self, entities):
        nearest_corpse = None
        min_distance = 10000000

        for entity in [entity for entity in entities if 'remains' in entity.name]:
            distance = entity.distance_to(entity)
            if distance < min_distance and distance < 50:
                nearest_corpse = entity
                min_distance = distance
        
        return nearest_corpse

ai_dictionary = {
    'Basic': BasicMonster,
    'Coward': Coward,
    'Scavenger': Scavenger
}

#TODO: Entities should have a concept of their friends. When their friends are fleeing, they should switch from friendly to hostile
# Also, Hostile should only render them hostile against their enemies