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
        