import tcod as libtcod
from game_messages import Message 

effects = {
    'Shredding': {
        'description': " with a serrated edge, caked with dried blood",
        "name": "of Shredding",
        "arrangement": "suffix",
        "targets": [5. 6],
        "hit_effect": ['Shredding']
    },
    'Healing': {
        ''
    }
}

def heal(*args, **kwargs):
    print(args)
    print(kwargs)
    entity = args[0]
    amount = kwargs.get('amount')

    if entity.get_component("Fighter").hp < entity.get_component("Fighter").max_hp:
        entity.get_component("Fighter").hp = min(entity.get_component("Fighter").max_hp, entity.get_component("Fighter").hp + amount)
    if entity.log:
        entity.log.add_message(Message('Healed {0} damage'.format(amount), libtcod.white))

item_fuction_dict = {
    "heal": heal
}