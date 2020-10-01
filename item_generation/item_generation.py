from .base_items import weapons, armor, weapon_weights, armor_weights
from .qualities  import qualities, quality_weights, item_equip_dict
from .item_functions import item_function_dict, effects, effect_weights
from components.item import Item
from entity import Entity
from render_functions import RenderOrder
from game_states import AIStates
import random

def generate_weapon(quality_prob, effect_prob, x, y, log):
    item_base = weapons[random.choices(list(weapons.keys()), weapon_weights)[0]].copy()
    if 'kwargs' not in item_base:
        item_base['kwargs'] = {}

    if 'equip_abilities' not in item_base:
        item_base['equip_abilities'] = []
    else:
        item_base['equip_abilities'] = [item_equip_dict[quality] for quality in item_base['equip_abilities']]

    if 'functions' not in item_base:
        item_base['functions'] = []
    else:
        item_base['functions'] = [item_function_dict[effect] for effect in item_base['functions']]

    if random.random() <= quality_prob:
        while True:
            quality = qualities[random.choices(list(qualities.keys()), quality_weights)[0]].copy()
            if item_base['type'] in quality['targets']:
                break
        apply_quality(item_base, quality)

    if random.random() <= effect_prob:
        while True:
            effect = effects[random.choices(list(effects.keys()), effect_weights)[0]].copy()
            if item_base['type'] in effect['targets']:
                break
        apply_effect(item_base, effect)

    format_name(item_base)
    components = {
        "Item": Item(use_function=item_base['functions'], uses=item_base['uses'], item_type=item_base['type'], equip_effects=item_base['equip_abilities'], strength=item_base['strength'], **item_base['kwargs'])
    }

    return Entity(x, y, item_base['icon'], item_base['color'], item_base['name'], blocks=False, render_order=RenderOrder.ITEM, message_log=log, state=AIStates.INANIMATE, components=components)


def apply_effect(item, effect):
    item['functions'] = item['equip_abilities'] + [item_function_dict[func] for func in effect['hit_effect']]
    item['effect_description'] = effect['description']
    item['effect_name'] = effect['name']
    item['kwargs'] = {**item['kwargs'], **effect['kwargs']}
    

def apply_quality(item, quality):
    item['equip_abilities'] = item['functions'] + [item_equip_dict[effect](**quality['kwargs']) for effect in quality['effects']]
    item['quality_description'] = quality['description']
    item['quality_name'] = quality['name']
    item['kwargs'] = {**item['kwargs'], **quality['kwargs']}

def format_name(item):
    print(item)
    item['name'] = item['name'].format(item['quality_name'] if 'quality_name' in item else '', item['effect_name'] if 'effect_name' in item else '')
    item['description'] = item['description'].format(item['quality_description'] if 'quality_description' in item else '', item['effect_description'] if 'effect_description' in item else '')

