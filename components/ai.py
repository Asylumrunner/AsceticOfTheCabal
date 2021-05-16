import tcod as libtcod

# A hold-all file for the various NPC behaviors, all of which are encapsulated within their own class
# Each behavior implements take_turn, describing what it should do when its turn comes around

class BasicMonster:
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
    def __init__(self):
        self.corpse = None
    
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner

        if not self.corpse:
            corpse = self.find_nearest_corpse(entities)

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2 and target.get_component("Fighter").get_health_percentage() < 0.5:
                monster.move_astar(target, entities, game_map)
            elif target.get_component("Fighter").hp > 0:
                monster.get_component("Fighter").attack(target)
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