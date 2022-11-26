from numpy import size
import tcod as libtcod
import game_constants
from utilities.csv_reader import read_csv_to_dict
from math import ceil
from random import choice

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
        self.log = message_log


    def build_city_limits(self):
        world_size = game_constants.size_world
        ws_percentage = game_constants.world_size_percentage
        #1. Instantiate a square world of N x N, where n=size_world
        world_map = [[True for x in range(world_size)] for y in range(world_size)]

        #self.print_map(world_map, "inital_map.txt")

        #2. Create a deletion candidates list of tuples, featuring every edge space (and corners twice)
        deletion_candidates = []
        for n in range(world_size):
            deletion_candidates.append((n,0))
            deletion_candidates.append((0, n))
            deletion_candidates.append((world_size-1, world_size-1-n))
            deletion_candidates.append((world_size-1-n, world_size-1))
        
        #3. Delete spaces by randomly selecting candidates out of deletion_candidates, then enqueuing their neighbors
        spaces_to_delete = ceil((world_size * world_size) * (1 - ws_percentage))
        print("Deleting {0} spaces out of {1}, conforming to world fill percentage of {2}".format(spaces_to_delete, (world_size * world_size), ws_percentage))
        for x in range(spaces_to_delete):
            print("Performing deletion {0}".format(x))
            space_selected = choice(deletion_candidates)
            world_map[space_selected[0]][space_selected[1]] = False
            deletion_candidates.remove(space_selected)

            if space_selected[0] > 0 and world_map[space_selected[0]-1][space_selected[1]]:
                deletion_candidates.append((space_selected[0]-1, space_selected[1]))

            if space_selected[0] < world_size-1 and world_map[space_selected[0]+1][space_selected[1]]:
                deletion_candidates.append((space_selected[0]+1, space_selected[1]))

            if space_selected[1] > 0 and world_map[space_selected[0]][space_selected[1]-1]:
                deletion_candidates.append((space_selected[0], space_selected[1]-1))

            if space_selected[1] < world_size-1 and world_map[space_selected[0]][space_selected[1]+1]:
                deletion_candidates.append((space_selected[0], space_selected[1]+1))

        self.print_map(world_map, "trimmed_map.txt")
        
        #4. Check for islands, picking the largest contiguous landmass
        unidentified_land = []
        identification_queue = []
        for x in range(world_size):
            for y in range(world_size):
                if world_map[x][y]:
                    unidentified_land.append((x, y))
        #print("Size of all valid land currently = {}".format(len(unidentified_land)))

        best_island = {
            "size": -1,
            "spaces": []
        }

        while unidentified_land:
            new_island = {
                "size": 0,
                "spaces": []
            }

            identification_queue.append(unidentified_land.pop(0))

            #print("Checking new island")
            while identification_queue:
                space_selected = identification_queue.pop(0)
                #print("Adding space {} to island".format(space_selected))

                new_island["size"] += 1
                new_island["spaces"].append(space_selected)

                if space_selected[0] > 0 and (space_selected[0]-1, space_selected[1]) in unidentified_land:
                    identification_queue.append((space_selected[0]-1, space_selected[1]))
                    unidentified_land.remove((space_selected[0]-1, space_selected[1]))
                    #print("Adding {} to identification queue [0]".format((space_selected[0]-1, space_selected[1])))
                
                if space_selected[0] < world_size-1 and (space_selected[0]+1, space_selected[1]) in unidentified_land:
                    identification_queue.append((space_selected[0]+1, space_selected[1]))
                    unidentified_land.remove((space_selected[0]+1, space_selected[1]))
                    #print("Adding {} to identification queue [1]".format((space_selected[0]+1, space_selected[1])))
                
                if space_selected[1] > 0 and (space_selected[0], space_selected[1]-1) in unidentified_land:
                    identification_queue.append((space_selected[0], space_selected[1]-1))
                    unidentified_land.remove((space_selected[0], space_selected[1]-1))
                    #print("Adding {} to identification queue [2]".format((space_selected[0], space_selected[1]-1)))
                
                if space_selected[1] < world_size-1 and (space_selected[0], space_selected[1]+1) in unidentified_land:
                    identification_queue.append((space_selected[0], space_selected[1]+1))
                    unidentified_land.remove((space_selected[0], space_selected[1]+1))
                    #print("Adding {} to identification queue [3]".format((space_selected[0], space_selected[1]+1)))
                
                #print("New size of unexplored land: {}".format(len(unidentified_land)))
                #print("Current size of discovery queue: {}".format(len(identification_queue)))
            
            #print("Size of complete island: {}".format(new_island["size"]))
            if new_island["size"] > best_island["size"]:
                #print("New island's size of {0} beats old best of {1}, replacing best island".format(new_island["size"], best_island["size"]))
                for space in best_island["spaces"]:
                    world_map[space[0]][space[1]] = False
                best_island = new_island
            
            else:
                for space in new_island["spaces"]:
                    world_map[space[0]][space[1]] = False
        
        self.print_map(world_map, "final_map.txt")

    def print_map(self, world_map, file_name):
        # Helper function that produces a file of the map in progress to check & debug
        with open("{}".format(file_name), "w") as outfile:
            for row in world_map:
                for column in row:
                    if column:
                        outfile.write("O")
                    else:
                        outfile.write(" ")
                outfile.write("\n")

            


