from numpy import size
import tcod as libtcod
import game_constants
from utilities.csv_reader import read_csv_to_dict
from math import ceil, floor, dist, sqrt
from random import choice, randrange
from pprint import PrettyPrinter

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

# TODO: Add timers to all this shit
class GameMap:
    def __init__(self, message_log):
        self.log = message_log

    def generate_map(self):
        self.construct_blocks()

    def construct_blocks(self):
        world_size = game_constants.size_world
        initial_block_size = game_constants.initial_block_size

        if initial_block_size > world_size:
            raise ValueError("Size of initial starting landmass cannot be larger than size of initial map")

        world_fill_percentage = game_constants.world_size_percentage

        filled_spaces = []
        #1. Instantiate an empty grid of blocks, then fill with the initial blob
        world_map = [[0 for x in range(world_size)] for y in range(world_size)]
        center_fill_count = world_size - initial_block_size
        for n in range(floor(center_fill_count/2), len(world_map) - ceil(center_fill_count/2)):
            for m in range(floor(center_fill_count/2), len(world_map) - ceil(center_fill_count/2)):
                world_map[n][m] = 1
                filled_spaces.append((n, m))

        #2. Append new blocks randomly onto the edges of the playable game space
        goal_world_size = ceil((world_size ** 2) * world_fill_percentage)
        print("Goal world size: {}".format(goal_world_size))
        while len(filled_spaces) < goal_world_size:
            space_to_build_upon = choice(filled_spaces)
            direction_to_build = randrange(0, 4)

            if direction_to_build == 0:
                new_space = (space_to_build_upon[0], space_to_build_upon[1] + 1)

            elif direction_to_build == 1:
                new_space = (space_to_build_upon[0], space_to_build_upon[1] - 1)

            elif direction_to_build == 2:
                new_space = (space_to_build_upon[0] + 1, space_to_build_upon[1])

            elif direction_to_build == 3:
                new_space = (space_to_build_upon[0] - 1, space_to_build_upon[1])

            if new_space not in filled_spaces and new_space[0] in range(0, world_size) and new_space[1] in range(0, world_size):
                world_map[new_space[0]][new_space[1]] = 1
                filled_spaces.append(new_space)
                #print("From space {}, got random selector {} and created space {}".format(space_to_build_upon, direction_to_build, new_space))
    
        #3. Identify spaces on the boundaries of the created land-mass, identifying what kind of edge they are for later population
        for x in range(world_size):
            for y in range(world_size):
                if (x, y) not in filled_spaces:
                    bit_flags = 0

                    # Check each neighbor and, if it exists, flip the corresponding flag bit
                    if (x+1, y) in filled_spaces:
                        bit_flags += 1
                    if (x-1, y) in filled_spaces:
                        bit_flags += 2
                    if (x, y+1) in filled_spaces:
                        bit_flags += 4
                    if (x, y-1) in filled_spaces:
                        bit_flags += 8
                    if (x+1, y+1) in filled_spaces:
                        bit_flags += 16
                    if (x+1, y-1) in filled_spaces:
                        bit_flags += 32
                    if (x-1, y+1) in filled_spaces:
                        bit_flags += 64
                    if (x-1, y-1) in filled_spaces:
                        bit_flags += 128
                    
                    print("point {} represented by binary bit flags {}".format((x, y), format(bit_flags, '#010b')))
                    world_map[x][y] = bit_flags + 1 if bit_flags != 0 else 0
                    
        self.print_edge_map(world_map, "initial_map.txt")

    # TODO: This don't scale at _all_ lmao
    def build_city_limits(self):
        world_size = game_constants.size_world
        ws_percentage = game_constants.world_size_percentage
        #1. Instantiate a square world of N x N, where n=size_world
        world_map = [[True for x in range(world_size)] for y in range(world_size)]

        self.print_map(world_map, "inital_map.txt")

        #2. Create a deletion candidates list of tuples, featuring every edge space (and corners twice)
        deletion_candidates = []
        for n in range(world_size):
            deletion_candidates.append((n,0))
            deletion_candidates.append((0, n))
            deletion_candidates.append((world_size-1, world_size-1-n))
            deletion_candidates.append((world_size-1-n, world_size-1))
        
        #3. Delete spaces by randomly selecting candidates out of deletion_candidates, then enqueuing their neighbors
        spaces_to_delete = ceil((world_size * world_size) * (1 - ws_percentage))
        #print("Deleting {0} spaces out of {1}, conforming to world fill percentage of {2}".format(spaces_to_delete, (world_size * world_size), ws_percentage))
        for x in range(spaces_to_delete):
            #print("Performing deletion {0}".format(x))
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
        return world_map
    
    def define_neighborhoods(self, world_map):
        #1. Generate N random "home" points for N neighborhoods
        num_neighborhoods = game_constants.number_of_neighborhoods
        world_size = game_constants.size_world
        neighborhood_cores = []

        while len(neighborhood_cores) < num_neighborhoods:
            candidate = (randrange(0, world_size),randrange(0, world_size))
            if world_map[candidate[0]][candidate[1]]:
                conflicting_cores = [core for core in neighborhood_cores if dist(core, candidate) <= 4]
                if not conflicting_cores:
                    neighborhood_cores.append(candidate)

        print("Cores placed at {}".format(neighborhood_cores))

        #2. Create N sets which will contain the points located in each neighborhood
        neighborhoods = [{"core": core, "points": [], "gates": []} for core in neighborhood_cores]

        #3. Calculate the closest core to each space on the world map, and assign that point to the neighborhood associated with that point
        for x in range(world_size):
            for y in range(world_size):
                if world_map[x][y]:
                    closest_core = -1
                    closest_core_distance = 100000000
                    for n in range(num_neighborhoods):
                        core_distance = dist((x,y), neighborhoods[n]["core"])
                        if core_distance < closest_core_distance:
                            closest_core = n
                            closest_core_distance = core_distance
                    neighborhoods[closest_core]["points"].append((x,y))

        #4. Mark spaces in each neighborhood as transition points to their adjacent neighborhoods by draing a line between cores
        for core_index in range(num_neighborhoods):
            other_core_index = core_index + 1
            while other_core_index < len(neighborhood_cores):
                line = self.bresenham_line(world_map, neighborhood_cores[core_index], neighborhood_cores[other_core_index])
                for n in range(len(line)-1):
                    if line[n] in neighborhoods[core_index]["points"] and line[n+1] in neighborhoods[other_core_index]["points"]:
                        neighborhoods[core_index]["gates"].append({
                            "point": line[n],
                            "destination": other_core_index
                        })
                        neighborhoods[other_core_index]["gates"].append({
                            "point": line[n+1],
                            "destination": core_index
                        })
                other_core_index += 1

        self.print_neighborhood_map(world_map, neighborhoods, "neighborhood_map.txt")

        #6. Divide neighborhoods into individual world map objects, locally normalizing their coordinate systems

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
    
    #TODO: Not hi-pri, but this runs like absolute dogass
    def print_neighborhood_map(self, world_map, neighborhoods, file_name):
        with open("{}".format(file_name), "w") as outfile:
            for row in range(len(world_map)):
                for column in range(len(world_map)):
                    if world_map[row][column]:
                        for n in range(len(neighborhoods)):
                            try:
                                if neighborhoods[n]["points"].index((row, column)) > -1:
                                    outfile.write("{}".format(n))
                            except ValueError:
                                pass
                    else:
                        outfile.write(" ")
                outfile.write("\n")

    def print_edge_map(self, world_map, file_name):
        with open("{}".format(file_name), "w") as outfile:
            for row in world_map:
                    for column in row:
                        if column == 1:
                            outfile.write("O")
                        elif column == 0:
                            outfile.write(" ")
                        else:
                            outfile.write("X")
                    outfile.write("\n")

    # TODO: Clean up this code a lil bit
    def bresenham_line(self, world_map, pt1, pt2):
        # Helper function which returns a list of the 2D grid coordinates approximating a line between two points
        # in accordance with the bresenham line-drawing algorithm https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
        start = pt1 if pt1[1] < pt2[1] else pt2
        finish = pt1 if start == pt2 else pt2
        rise = finish[0] - start[0]
        run = finish[1] - start[1]

        # Condition for straight vertical lines
        if run == 0:
            return [(start[1], x) for x in range(min(start[0], finish[0]), max(start[0], finish[0])+1)]
            
        slope = float(rise/run)
        line = []
        y = start[0]
        lift = 0.0

        # Basically, depending on whether rise or run is greater, and then on if slope is positive or negative
        # We determine the line by starting with the leftmost point, and then we either:
        # 1. if rise is greater than run, then we increment y every iteration, then add the inverse of the slope
        #    to an error value called lift. When lift cracks the threshold (interval) to round up, we finally increment
        #    x before the next iteration
        # 2. if run is greater than rise, as above, but swap x and y
        if abs(slope) >= 1 and slope >= 0:
            print("entering case 1")
            interval = 0.5
            for x in range(start[1], finish[1]+1):
                while lift < interval:
                    if world_map[y][x]:
                        line.append((y, x))
                    lift += float(1/slope)
                    y += 1
                interval += 1

        elif abs(slope) >= 1 and slope < 0:
            print("entering case 2")
            interval = -0.5
            for x in range(start[1], finish[1]+1):
                while lift > interval:
                    if world_map[y][x]:
                        line.append((y, x))
                    lift += float(1/slope)
                    y -= 1
                interval -= 1
        elif abs(slope) < 1 and slope >= 0:
            print("entering case 3")
            interval = 0.5
            for x in range(start[1], finish[1]+1):
                if world_map[y][x]:
                    line.append((y, x))
                
                lift += slope
                if lift > interval:
                    y += 1
                    interval += 1
        elif abs(slope) < 1 and slope < 0:
            print("entering case 4")
            interval = -0.5
            for x in range(start[1], finish[1]+1):
                if world_map[y][x]:
                    line.append((y, x))
                
                lift += slope
                if lift < interval:
                    y -= 1
                    interval -= 1
        
        if start != pt1:
            line.reverse()

        return line
                

                



            
            

    



            


