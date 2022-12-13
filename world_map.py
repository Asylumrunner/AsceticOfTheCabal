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
        self.world_map = None

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
        self.print_map(world_map, "initial_map.txt")
    
        #3. Identify spaces on the boundaries of the created land-mass, identifying what kind of edge they are for later population
        for x in range(world_size):
            for y in range(world_size):
                if (x, y) not in filled_spaces:
                    bit_flags = 0

                    # Check each neighbor and, if it exists, flip the corresponding flag bit
                    if (x+1, y) in filled_spaces: # Below
                        bit_flags += 2
                    if (x-1, y) in filled_spaces: # Above
                        bit_flags += 4
                    if (x, y+1) in filled_spaces: # Right
                        bit_flags += 8
                    if (x, y-1) in filled_spaces: # Left
                        bit_flags += 16
                    
                    #print("point {} represented by binary bit flags {}".format((x, y), format(bit_flags, '#010b')))
                    world_map[x][y] = bit_flags + 1 if bit_flags != 0 else 0
        
        #4. Identify neighborhood cores
        neighborhood_cores = []
        while len(neighborhood_cores) < game_constants.number_of_neighborhoods:
            potential_core = choice(filled_spaces)
            if potential_core not in neighborhood_cores:
                neighborhood_cores.append(potential_core)
        
        #5. Repopulate the world map with block objects
        for x in range(world_size):
            for y in range(world_size):
                space_code = world_map[x][y]
                neighborhood_code = []
                if space_code != 0:
                    closest_neighborhood_core = []
                    closest_core_distance = 100
                    for index in range(len(neighborhood_cores)):
                        dist_to_core = dist((x, y), neighborhood_cores[index])
                        if dist_to_core == closest_core_distance:
                            closest_neighborhood_core.append(neighborhood_cores[index])
                        elif dist_to_core < closest_core_distance:
                            closest_core_distance = dist_to_core
                            closest_neighborhood_core = [neighborhood_cores[index]]
                    neighborhood_code = closest_neighborhood_core
                
                world_map[x][y] = Block(space_code, neighborhood_code)


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

        return 
        
class Block:
    def __init__(self, code=0, neighborhood=0):
        self.block_type_code = code
        self.neighborhood = neighborhood

        # TODO: Select a template from the template files and save its values here
        
        # TODO: With the template and the neighborhood, populate the template with stuff
