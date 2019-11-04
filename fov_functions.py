import tcod as libtcod
import game_constants

def initialize_fov(game_map):
    fov_map = libtcod.map.Map(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            fov_map.transparent[y][x] = not game_map.tiles[x][y].block_sight
            fov_map.walkable[y][x] = not game_map.tiles[x][y].blocked
    return fov_map

def recompute_fov(fov_map, x, y):
    fov_map.compute_fov(x, y, game_constants.fov_radius, game_constants.fov_light_walls, game_constants.fov_algorithm)
