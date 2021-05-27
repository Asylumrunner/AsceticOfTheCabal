class Tile:

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

        self.entities_contained = set()

        self.dijkstra_map_values = {
            'player': 9999999,
            'stairs': 9999999
        }

    def get_entities(self):
        return self.entities_contained

    def add_entity(self, entity):
        self.entities_contained.add(entity)
        
    def remove_entity(self, entity):
        self.entities_contained.discard(entity)
