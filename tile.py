class Tile:

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

        self.entities_contained = set()

        self.dijkstra_map_values = {}

    def get_entities(self):
        return self.entities_contained

    def add_entity(self, entity):
        self.entities_contained.add(entity)
        
    def remove_entity(self, entity):
        self.entities_contained.discard(entity)
    
    def set_dijkstra_map_value(self, key, value):
        self.dijkstra_map_values[key] = value

    def get_dijkstra_map_value(self, key):
        return self.dijkstra_map_values[key]
    
    def get_dijkstra_map_values(self):
        return self.dijkstra_map_values

    def set_dijkstra_map_values(self, values):
        self.dijkstra_map_values = values
