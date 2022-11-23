import tcod as libtcod
import game_constants
from utilities.csv_reader import read_csv_to_dict

""" 
This function runs only once at world gen, and thus can be a bit of a beefier boy, and store a bunch of data
TODOS:
1. Generate a large flat plane map, larger than the screen
2. Populate that map with structures (I think for the moment, structures will be separate maps) from random gen lists
2A. Place those structures logically within the game world
3. Populate the overworld map with NPCs
4. Populate the map with doodads
5. Dunno where this should go, but the map should probably be built in chunks, such that individual chunks can be loaded and de-loaded
"""
class GameMap:
    def __init__(self, message_log):
        self.width = game_constants.world_width
        self.height = game_constants.world_height
        self.tiles = self.initialize_tiles()
        self.log = message_log
        self.floor_dict = self.get_floor_info()

        building_templates = read_csv_to_dict("./data/buildings.csv")

