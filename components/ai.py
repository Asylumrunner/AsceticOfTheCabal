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

ai_dictionary = {
    'Basic': BasicMonster,
    'Coward': Coward
}

#TODO: Entities should have a concept of their friends. When their friends are fleeing, they should switch from friendly to hostile
# Also, Hostile should only render them hostile against their enemies