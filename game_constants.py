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
        'conv': {
            'utterance': 'Did you know Coca Cola is made with real cocaine?',
            'choices': [
                {
                    'player_utterance': 'No it\'s coca leaves, not cocaine',
                    'response': {
                        'utterance': 'Whatever, fuck you man',
                        'choices': []
                    }
                },
                {
                    'player_utterance': 'Where\'d you learn that?',
                    'response': {
                        'utterance': 'Joe Rogan podcast, dude. Check it out',
                        'choices': [
                            {
                                'player_utterance': 'Isn\'t Joe Rogan that crazy guy who talks about DMT?',
                                'response': {
                                    'utterance': 'Not wrong.',
                                    'choices': []
                                }
                            }
                        ]
                    }
                }
            ]
        },
        'money': 10
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
        'money': 30
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
        'conv': {
            'utterance': 'Begone human. My observations must be unimpeded',
            'choices': []
        }
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
        'conv': {
            'utterance': 'Howdy stranger! Welcome to town! What brings you here?',
            'choices': [
                {
                    'player_utterance': 'Just passin\' through.',
                    'response': {
                        'utterance': "Well, be sure to go pray to the City God before you leave!",
                        'choices': []
                    }
                },
                {
                    'player_utterance': "I worship the Cabal. I'm here to kill your God",
                    'response': {
                        'utterance': "GUARDS! GUARDS! HERETIC!",
                        'choices': []
                    }
                }
            ]
        }
    },
    'Godspawn': {
        'icon': 'G',
        'color': libtcod.dark_red,
        'name': "Godspawn",
        'hp': 15,
        'defense': 1,
        'power': 7,
        'state': AIStates.HOSTILE,
        'description': 'A hulking mass, humanoid, but resembling the God of this City. One of its children',
        'money': 0
    }
}

items = {
    'Healing Potion': {
        'icon': '!',
        'color': libtcod.violet,
        'name': 'Healing Potion',
        'uses': 1,
        'type': 1,
        'functions': ['heal'],
        'kwargs': {
            'amount': 30
        }
    }
}

floors = {
    (1, 2, 3): {
        'enemies': {
            'names': ['Citizen', 'Godspawn', 'Troll', 'Eye of the Divine'],
            'distribution': [0.69, 0.01, 0.2, 0.1]
        },
        'colors': {
            'dark_wall': libtcod.dark_grey,
            'dark_ground': libtcod.sepia,
            'light_wall': libtcod.light_grey,
            'light_ground': libtcod.lighter_sepia
        }
    },
    (4, 5, 6): {
        'enemies': {
            'names': ['Orc', 'Troll'],
            'distribution': [0.7, 0.3]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        }
    },
    (7, 8, 9): {
        'enemies': {
            'names': ['Orc', 'Troll'],
            'distribution': [0.7, 0.3]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        }
    },
    (10, 11): {
        'enemies': {
            'names': ['Orc', 'Troll'],
            'distribution': [0.7, 0.3]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        }
    },
    (12,): {
        'enemies': {
            'names': ['Orc', 'Troll'],
            'distribution': [0.7, 0.3]
        },
        'colors': {
            'dark_wall': libtcod.darker_grey,
            'dark_ground': libtcod.dark_sepia,
            'light_wall': libtcod.grey,
            'light_ground': libtcod.light_sepia
        }
    }
}