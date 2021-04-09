import tcod as libtcod
import game_constants

# handles the computation of the FOV map, determining what the player can see

def initialize_fov(game_map):
    # returns an FOV map baseline based on which tiles are and are not walkable and/or see-through
    fov_map = libtcod.map.Map(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            fov_map.transparent[y][x] = not game_map.tiles[x][y].block_sight
            fov_map.walkable[y][x] = not game_map.tiles[x][y].blocked
    return fov_map

# computes the current FOV based on the player's location in the map
def recompute_fov(fov_map, x, y):
    fov_map.compute_fov(x, y, game_constants.fov_radius, game_constants.fov_light_walls, game_constants.fov_algorithm)
