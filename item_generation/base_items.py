import tcod as libtcod

# Lists of the base (unenchanted) weapons and armor descriptions, as well as probability lists of how likely they are to appear

weapons = {
    "Sword": {
        'name': '{}Sword{}',
        'description': 'A {}longsword{}',
        'uses': -99,
        'type': 5,
        'strength': 5,
        'icon': 'T',
        'price': 5,
        'color': libtcod.light_blue
    },
    "Axe": {
        'name': '{}Axe{}',
        'description': 'A hefty {}axe{}',
        'uses': -99,
        'type': 5,
        'strength': 10,
        'icon': 'P',
        'price': 10,
        'color': libtcod.light_blue
    },
    "Knife": {
        'name': '{}Knife{}',
        'description': 'A serrated {}knife{}',
        'uses': -99,
        'type': 5,
        'strength': 3,
        'hit_abilities': ['Backstab'],
        'icon': 't',
        'price': 3,
        'color': libtcod.light_blue

    }
}

starting_pistol = {
    'name': 'Ascetic\'s Pistol',
    'description': 'Given to you by the Cabal at the start of your pilgrimmage',
    'uses': -99,
    'type': 6,
    'strength': 3,
    'icon': 'r',
    'price': 1,
    'color': libtcod.red,
    'functions': [],
    'equip_abilities': [],
    'kwargs': {
        'ammo': 6
    }
}

weapon_weights = [2, 1, 3]

armor = {
    "Hat": {
        'name': 'Hat',
        'description': 'A slightly-worn {}cap{}',
        'uses': -99,
        'type': 1,
        'defense': 3,
        'icon': 'A',
        'price': '10',
        'color': libtcod.light_green
    }
}

armor_weights = [1]

potions = {
    'Potion': {
        'icon': '!',
        'color': libtcod.red,
        'description': "A vial of mysterious {}liquid",
        'name': 'Potion{}',
        'uses': 1,
        'type': 0,
        'strength': 0,
        'price': 10,
        'equip_abilities': [],
        'functions': [],
        'kwargs': {}
    },
    'Big Potion': {
        'icon': '?',
        'color': libtcod.red,
        'description': 'A large phial of mysterious {}liquid',
        'name': 'Big Potion{}',
        'uses': 3,
        'type': 0,
        'strength': 0,
        'price': 25,
        'equip_abilities': [],
        'functions': [],
        'kwargs': {}
    }
}

potion_weights = [4, 1]