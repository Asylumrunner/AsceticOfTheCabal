
# A class designed to hold and maintain all of the entities in the game, providing a one-stop shop
# Is tightly linked to the Game Map, since entity locations are double-stored here and on the map
class Entities():
    def __init__(self, game_map):
        self.game_map = game_map

        self.entity_set = set()

    # Returns a list version of the entity set
    # Changes to this list will not reflect changes to the original
    def get_entity_set(self):
        return list(self.entity_set)

    # Inserts an entity into the set, and adds a reference to it on the appropriate map tile
    # Both this class's entity set and the tile's are sets, so there shouldn't be any concern for double-dipping
    def insert_entity(self, entity):
        self.entity_set.add(entity)
        self.game_map.add_entity_to_map(entity, entity.x, entity.y)
    
    # Removes an entity from the entity list, and removes the reference to it on the appropriate map tile
    # Both this class's entity set and the tile's are sets using discard, so there should be no concern for a false removal
    def remove_entity(self, entity):
        self.entity_set.discard(entity)
        self.game_map.remove_entity_from_map(entity, entity.x, entity.y)

    # Returns a sublist of the entity set, as a list, that passes some lambda conditional function that returns True/False
    # Default argument will just return the set as a list
    def get_sublist(self, selector_function=lambda x: x==x):
        entities_as_list = list(self.entity_set)
        return [entity for entity in entities_as_list if selector_function(entity)]

    # Returns true if anything in the entity set matches the given condition
    # Otherwise returns false
    def get_any_condition(self, selector_function=lambda x: x==x):
        for entity in list(self.entity_set):
            if selector_function(entity):
                return True
        return False
    
    # A convenience function that sets the game log of every entity in the game to the same log
    # This resolves some game log weirdness after loading the game
    def set_log_all(self, game_log):
        for entity in self.get_entity_set():
            if entity.get_log() != game_log:
                entity.log = game_log