# Credit to Red Blob Games for this logic, found at https://www.redblobgames.com/grids/line-drawing.html
# Is used to determine if a character has unimpeded line of sight to another character
def draw_line(point1, point2):
    line = []
    interpolation_points = diagonal_distance(point1, point2)
    for x in range(interpolation_points):
        int_co = 0 if x == 0 else x/interpolation_points
        line.append(round_point_to_grid(lerp_point(point1, point2, int_co)))
    return line

def diagonal_distance(tuple1, tuple2):
    dx = abs(tuple2[0] - tuple1[0])
    dy = abs(tuple2[1] - tuple1[1])
    return max(dx, dy)

def round_point_to_grid(point):
    return (round(point[0]), round(point[1]))

def lerp(val1, val2, interpolation_coefficient):
    return (interpolation_coefficient * val1) + ((1-interpolation_coefficient) * val2)

def lerp_point(point1, point2, coefficient):
    return (lerp(point1[0], point2[0], coefficient), lerp(point1[1], point2[1], coefficient))