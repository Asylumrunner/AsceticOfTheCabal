class Entities():
    def __init__(self, game_map):
        self.game_map = game_map

        self.entity_set = set()

    # Returns a list version of the entity set
    # Changes to this list will not reflect changes to the original
    def get_entity_set(self):
        return list(self.entity_set)

    def insert_entity(self, entity):
        self.entity_set.add(entity)
        self.game_map.add_entity_to_map(entity, entity.x, entity.y)
    
    def remove_entity(self, entity):
        self.entity_set.discard(entity)
        self.game_map.remove_entity_from_map(entity, entity.x, entity.y)