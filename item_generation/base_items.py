weapons = {
    "Sword": {
        'name': 'Sword',
        'desc_start': 'A longsword',
        'uses': -99,
        'type': 5,
        'strength': 5
    },
    "Axe": {
        'name': 'Axe',
        'desc_start': 'A hefty axe',
        'uses': -99,
        'type': 5,
        'strength': 10
    },
    "Knife": {
        'name': 'Knife',
        'desc_start': 'A serrated knife',
        'uses': -99,
        'type': 5,
        'strength': 3,
        'hit_abilities': ['Backstab']
    }
}

armor = {
    "Hat": {
        'name': 'Hat',
        'desc_start': 'A slightly-worn cap',
        'uses': -99,
        'type': 1,
        'equip_abilities': ['Armor'],
        'kwargs': {
            'armor': 2
        }
    }
}