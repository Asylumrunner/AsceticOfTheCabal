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
    },
    'Avaricial': {
        'description': " with a slight magnetic pull, drawing the coinpurse from your satchel",
        "name": " of Avarice",
        "arrangement": "suffix",
        "targets": [5, 6],
        "hit_effect": ["avaricial"],
        'kwargs': {}
    },
    'Shredding': {
        'description': " covered in barbs that look like they could dig in deep into flesh",
        "name": " of Shredding",
        "arrangement": "suffix",
        "targets": [5],
        "hit_effect": ["shredding"],
        "kwargs": {
            'amount': 5
        }
    }
}

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    if entity.get_component("Fighter").hp < entity.get_component("Fighter").max_hp:
        entity.get_component("Fighter").hp = min(entity.get_component("Fighter").max_hp, entity.get_component("Fighter").hp + amount)
    if entity.log:
        entity.log.add_message(Message('{} healed {} damage'.format(entity.name, amount), libtcod.white))

def hematic(*args, **kwargs):
    entity = args[0]
    target = args[1]
    blood = random.randint(0, 5)
    entity.get_component("Fighter").take_damage(blood)
    target.get_component("Fighter").take_damage(blood * 2)

    if blood > 0:
        entity.log.add_message(Message('Drained {} blood from the wielder to deal {} damage to {}'.format(blood, blood*2, target.name)))
    
def avaricial(*args, **kwargs):
    entity = args[0]
    target = args[1]
    money_drawn = random.randint(0, 5)
    if(entity.get_component("Fighter").money >= money_drawn):
        entity.get_component("Fighter").money -= money_drawn
        target.get_component("Fighter").take_damage(money_drawn * 2)

        if money_drawn > 0:
            entity.log.add_message(Message('Drained {} dollars from the wielder to deal {} damage to {}'.format(money_drawn, money_drawn*2, target.name)))
    
def shredding(*args, **kwargs):
    entity = args[0]
    target = args[1]

    if target.has_component("StatusContainer"):
        target.get_component("StatusContainer").inflict_status('bleeding', kwargs['amount'])
        entity.log.add_message(Message('Barbs dig into {}, causing it to bleed'.format(target.name)))

item_function_dict = {
    "heal": heal,
    "hematic": hematic,
    "avaricial": avaricial,
    "shredding": shredding
}

effect_weights = [1, 1, 1, 100]