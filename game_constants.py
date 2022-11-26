import tcod as libtcod
from game_states import AIStates

screen_width = 120
screen_height = 75

bar_width = 20
panel_height = 12
panel_y = screen_height - panel_height

message_x = bar_width + 2
message_width = screen_width - bar_width - 2
message_height = panel_height - 1

inventory_width = 50

map_width = screen_width
map_height = panel_y-1

size_world = 100
world_size_percentage = 0.5

room_max_size = 10
room_min_size = 6
max_rooms = 30

fov_algorithm = libtcod.FOV_PERMISSIVE(4)
fov_light_walls = True
fov_radius = 10

max_monsters_per_room = 3
max_items_per_room = 1

character_portrait_width = 12

main_menu_background_image = libtcod.image_load('cool_background.png')

colors = {
    'dark_wall': libtcod.darker_grey,
    'dark_ground': libtcod.dark_sepia,
    'light_wall': libtcod.grey,
    'light_ground': libtcod.light_sepia
}

npcs = {
    'Orc': {
        'icon': 'o',
        'color': libtcod.desaturated_green,
        'name': 'Orc',
        'hp': 10,
        'defense': 0,
        'power': 3,
        'state': AIStates.FRIENDLY,
        'description': 'A lumbering green orc, with jagged teeth and a dim expression',
        'money': 10,
        'abilities': [],
        'ai': 'Basic',
        'factions': [4],
        'allies': [3, 4],
        'enemies': [],
        'blood': "blood"
    },
    'Troll': {
        'icon': 'T',
        'color': libtcod.darker_green,
        'name': 'Troll',
        'hp': 16,
        'defense': 1,
        'power': 4,
        'state': AIStates.HOSTILE,
        'description': 'A massive troll, standing two men tall. Brandishing a large club',
        'money': 30,
        'abilities': [],
        'ai': 'Basic',
        'factions': [],
        'allies': [],
        'enemies': [],
        'blood': "blood"
    },
    'Eye of the Divine': {
        'icon': libtcod.CHAR_FEMALE,
        'color': libtcod.dark_purple,
        'name': 'Eye of the Divine',
        'hp': 30,
        'defense': 3,
        'power': 5,
        'state': AIStates.FRIENDLY,
        'description': 'A tall, gaunt figure in a dark robe, with a mask of a single eye. Looks unhuman',
        'money': 100,
        'conv': '1',
        'abilities': ['heal'],
        'ai': 'Basic',
        'factions': [],
        'allies': [],
        'enemies': [],
        'blood': "godblood"
    },
    'Citizen': {
        'icon': 'a',
        'color': libtcod.white,
        'name': 'Citizen',
        'hp': 5,
        'defense': 0,
        'power': 2,
        'state': AIStates.FRIENDLY,
        'description': 'A human inhabitant of this city. Looks tired and dissheveled',
        'money': 10,
        'conv': 2,
        'abilities': [],
        'ai': 'Coward',
        'factions': [],
        'allies': [],
        'enemies': [],
        'blood': "blood"
    },
    'Godspawn': {
        'icon': 'G',
        'color': libtcod.dark_red,
        'name': "Godspawn",
        'hp': 5,
        'defense': 1,
        'power': 7,
        'state': AIStates.HOSTILE,
        'description': 'A hulking mass, humanoid, but resembling the God of this City. One of its children',
        'money': 0,
        'abilities': ['hematic'],
        'ai': 'Basic',
        'factions': [],
        'allies': [],
        'enemies': [],
        'blood': "godblood"
    },
    'Jeff Shopkeep': {
        'icon': 'S',
        'color': libtcod.light_green,
        'name': "Jeff Shopkeep",
        'hp': 9,
        'defense': 0,
        'power': 5,
        'state': AIStates.FRIENDLY,
        'description': 'A guy in a big coat who keeps goin Eyyyy gonna buy somethin gabagool',
        'shop_description': "Fuck you buy my garbage",
        'money': 10,
        'conv': 5,
        'shop': 'Default',
        'abilities': [],
        'ai': 'Coward',
        'factions': [],
        'allies': [],
        'enemies': [],
        'blood': "blood"
    },
    'Gravemite': {
        'icon': 'g',
        'color': libtcod.grey,
        'name': 'Gravemite',
        'hp': 4,
        'defense': 0,
        'power': 3,
        'state': AIStates.HOSTILE,
        'description': 'A ghoulish hunched-over humanoid with pale skin and caked-on blood around its mouth',
        'money': 0,
        'abilities': [],
        'ai': 'Scavenger',
        'factions': [],
        'allies': [],
        'enemies': [],
        'blood': "blood"
    },
    'Police Officer': {
        'icon': 'C',
        'color': libtcod.light_blue,
        'name': 'Police Officer',
        'hp': 12,
        'defense': 1,
        'power': 4,
        'state': AIStates.FRIENDLY,
        'description': 'A unformed police officer with a baton, wearing a shining badge and the sigil of the City God',
        'money': 10,
        'abilities': [],
        'ai': 'Basic',
        'conv': 7,
        'factions': [],
        'allies': [],
        'enemies': [],
        'blood': "blood"
    }
}

fluids = {
    'blood': {
        'name': 'pool of blood',
        'color': libtcod.dark_red,
        'conductive': True,
        'statuses': [],
        'time': 0
    },
    'water': {
        'name': 'water',
        'color': libtcod.light_blue,
        'conductive': True,
        'statuses': [],
        'time': 0
    },
    'godblood': {
        'name': 'pool of godblood',
        'color': libtcod.purple,
        'conductive': False,
        'statuses': [],
        'time': 0
    },
    'poison_waste': {
        'name': 'puddle of poisonous slime',
        'color': libtcod.green,
        'conductive': False,
        'statuses': ['posioned'],
        'time': 5
    }
}

shops = {
    'Default': [
        {
            'icon': 'a',
            'color': libtcod.lighter_red,
            'description': "A cool hat that makes you feel like a cool guy",
            'name': 'Cool Hat',
            'uses': -99,
            'type': 1,
            'functions': [],
            'cost': 10,
            'strength': 0,
            'defense': 1,
            'equip_abilities': [],
            'kwargs': {}
        },
        {
            'icon': 'a',
            'color': libtcod.lighter_red,
            'description': "A cool hat that makes you feel like a cool guy",
            'name': 'Cooler Hat',
            'uses': -99,
            'type': 1,
            'functions': [],
            'cost': 15,
            'strength': 0,
            'defense': 2,
            'equip_abilities': [],
            'kwargs': {}
        },
        {
            'icon': 'a',
            'color': libtcod.lighter_red,
            'description': "A cool hat that makes you feel like a cool guy",
            'name': 'Coolest Hat',
            'uses': -99,
            'type': 1,
            'functions': [],
            'cost': 20,
            'strength': 0,
            'defense': 3,
            'equip_abilities': [],
            'kwargs': {}
        }
    ]
}

items = {
    'Healing Potion': {
        'icon': '!',
        'color': libtcod.violet,
        'description': "A vial of stomach-churning green fluid, heals some health",
        'name': 'Healing Potion',
        'uses': 1,
        'type': 0,
        'strength': 0,
        'price': 10,
        'equip_abilities': [],
        'functions': [],
        'kwargs': {
            'amount': 30
        }
    },
    'Cool Hat': {
        'icon': 'a',
        'color': libtcod.lighter_red,
        'description': "A cool hat that makes you feel like a cool guy",
        'name': 'Cool Hat',
        'uses': -99,
        'type': 1,
        'functions': [],
        'equip_abilities': ['Armor', "Max_Health_Up"],
        'kwargs': {
            'armor': 5,
            'health_up': 10
        }
    }
}

floors = {
    (1, 2, 3): {
        'minor_enemies': {
            'names': ['Troll', 'Gravemite', 'Police Officer'],
            'distribution': [0.25, 0.25, 0.5]
        },
        'med_enemies': {
            'names': ['Godspawn'],
            'distribution': [1]
        },
        'major_enemies': {
            'names': [],
            'distribution': []
        },
        'shopkeeper': {
            'names': ['Jeff Shopkeep'],
            'distribution': [1]
        },
        'neutrals': {
            'names': ['Citizen', 'Eye of the Divine'],
            'distribution': [0.5, 0.5]
        },
        'colors': {
            'dark_wall': libtcod.dark_grey,
            'dark_ground': libtcod.sepia,
            'light_wall': libtcod.light_grey,
            'light_ground': libtcod.lighter_sepia
        },
        'quality_prob': 0.3,
        'effect_prob': 0.1
    },
    (4, 5, 6): {
        'minor_enemies': {
            'names': ['Troll', 'Gravemite'],
            'distribution': [1, 1]
        },
        'med_enemies': {
            'names': ['Godspawn'],
            'distribution': [1]
        },
        'major_enemies': {
            'names': [],
            'distribution': []
        },
        'shopkeeper': {
            'names': ['Jeff Shopkeep'],
            'distribution': [1]
        },
        'neutrals': {
            'names': ['Citizen', 'Eye of the Divine'],
            'distribution': [0.5, 0.5]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        },
        'quality_prob': 0.4,
        'effect_prob': 0.2
    },
    (7, 8, 9): {
        'minor_enemies': {
            'names': ['Troll', 'Gravemite'],
            'distribution': [0.75, 0.25]
        },
        'med_enemies': {
            'names': ['Godspawn'],
            'distribution': [1]
        },
        'major_enemies': {
            'names': [],
            'distribution': []
        },
        'shopkeeper': {
            'names': ['Jeff Shopkeep'],
            'distribution': [1]
        },
        'neutrals': {
            'names': ['Citizen', 'Eye of the Divine'],
            'distribution': [0.5, 0.5]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        },
        'quality_prob': 0.5,
        'effect_prob': 0.30
    },
    (10, 11): {
        'minor_enemies': {
            'names': ['Troll'],
            'distribution': [1]
        },
        'med_enemies': {
            'names': ['Godspawn'],
            'distribution': [1]
        },
        'major_enemies': {
            'names': [],
            'distribution': []
        },
        'shopkeeper': {
            'names': ['Jeff Shopkeep'],
            'distribution': [1]
        },
        'neutrals': {
            'names': ['Citizen', 'Eye of the Divine'],
            'distribution': [0.5, 0.5]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        },
        'quality_prob': 0.8,
        'effect_prob': 0.5
    },
    (12,): {
        'minor_enemies': {
            'names': ['Troll'],
            'distribution': [1]
        },
        'med_enemies': {
            'names': ['Godspawn'],
            'distribution': [1]
        },
        'major_enemies': {
            'names': [],
            'distribution': []
        },
        'shopkeeper': {
            'names': ['Jeff Shopkeep'],
            'distribution': [1]
        },
        'neutrals': {
            'names': ['Citizen', 'Eye of the Divine'],
            'distribution': [0.5, 0.5]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        },
        'quality_prob': 0.9,
        'effect_prob': 0.75
    }
}

default_border = {
    'top_and_bottom': '=',
    'side': '|',
    'corner': 'X'
}

shop_border = {
    'top_and_bottom': '~',
    'side': '|',
    'corner': '$'
}

death_border = {
    'top_and_bottom': 'X',
    'side': 'X',
    'corner': 'X'
}

status_border = {
    'top_and_bottom': '=',
    'side': '|',
    'corner': 'O'
}