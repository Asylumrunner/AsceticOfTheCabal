import tcod as libtcod

# Lists of the base (unenchanted) weapons and armor descriptions, as well as probability lists of how likely they are to appear

weapons = {
    "Sword": {
        'name': '{}Sword{}',
        'description': 'A {} longsword{}',
        'uses': -99,
        'type': 5,
        'strength': 5,
        'icon': 'T',
        'price': 5,
        'color': libtcod.light_blue
    },
    "Axe": {
        'name': '{}Axe{}',
        'description': 'A hefty {} axe{}',
        'uses': -99,
        'type': 5,
        'strength': 10,
        'icon': 'P',
        'price': 10,
        'color': libtcod.light_blue
    },
    "Knife": {
        'name': '{}Knife{}',
        'description': 'A serrated  {} knife{}',
        'uses': -99,
        'type': 5,
        'strength': 3,
        'hit_abilities': ['Backstab'],
        'icon': 't',
        'price': 3,
        'color': libtcod.light_blue

    }
}

weapon_weights = [2, 1, 3]

armor = {
    "Hat": {
        'name': 'Hat',
        'description': 'A slightly-worn cap',
        'uses': -99,
        'type': 1,
        'defense': 3,
        'icon': 'A',
        'price': '10',
        'color': libtcod.light_green
    }
}

armor_weights = [1]