import tcod as libtcod
import random
from game_messages import Message 

# A central repository for all of the on-use effects that might be enchanted onto a target

effects = {
    'Healing': {
        'description': " with a warm glow about it that makes you feel calm",
        "name": " of Healing",
        "arrangement": "suffix",
        "targets": [5,6],
        "hit_effect": ['heal'],
        'kwargs': {
            'amount': 5
        }
    },
    'Hematic': {
        'description': " with barbs which dig into your skin that seem to be drawing blood",
        "name": " of Blooddrinking",
        "arrangement": "suffix",
        "targets": [5,6],
        "hit_effect": ["hematic"],
        'kwargs': {}
    }
}

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    if entity.get_component("Fighter").hp < entity.get_component("Fighter").max_hp:
        entity.get_component("Fighter").hp = min(entity.get_component("Fighter").max_hp, entity.get_component("Fighter").hp + amount)
    if entity.log:
        entity.log.add_message(Message('Healed {0} damage'.format(amount), libtcod.white))

def hematic(*args, **kwargs):
    entity = args[0]
    target = args[1]
    blood = random.randint(0, 5)
    entity.get_component("Fighter").take_damage(blood)
    target.get_component("Fighter").take_damage(blood * 2)

    if blood > 0:
        entity.log.add_message(Message('Drained {} blood from the wielder to deal {} damage to {}'.format(blood, blood*2, target.name)))
    

item_function_dict = {
    "heal": heal,
    "hematic": hematic
}

effect_weights = [1, 1]