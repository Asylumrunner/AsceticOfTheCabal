import tcod as libtcod

screen_width = 80
screen_height = 50

bar_width = 20
panel_height = 7
panel_y = screen_height - panel_height

message_x = bar_width + 2
message_width = screen_width - bar_width - 2
message_height = panel_height - 1

inventory_width = 50

map_width = 80
map_height = 43

room_max_size = 10
room_min_size = 6
max_rooms = 30

fov_algorithm = libtcod.FOV_PERMISSIVE(4)
fov_light_walls = True
fov_radius = 10

max_monsters_per_room = 3
max_items_per_room = 1

colors = {
    'dark_wall': libtcod.Color(0, 0, 100),
    'dark_ground': libtcod.Color(50, 50, 150),
    'light_wall': libtcod.Color(130, 110, 50),
    'light_ground': libtcod.Color(200, 180, 50)
}

npcs = {
    'Orc': {
        'icon': 'o',
        'color': libtcod.desaturated_green,
        'name': 'Orc',
        'hp': 10,
        'defense': 0,
        'power': 3
    },
    'Troll': {
        'icon': 'T',
        'color': libtcod.darker_green,
        'name': 'Troll',
        'hp': 16,
        'defense': 1,
        'power': 4
    }
}

items = {
    'Healing Potion': {
        'icon': '!',
        'color': libtcod.violet,
        'name': 'Healing Potion',
        'uses': 1,
        'functions': ['heal'],
        'kwargs': {
            'amount': 30
        }
    }
}