from base_items import weapons, armor, weapon_weights, armor_weights
from qualities  import qualities, quality_weights
from item_functions import item_function_dict, effects, effect_weights
import random

def generate_weapon(quality_prob, effect_prob, x, y, log):
    item_base = random.choices(list(weapons.keys()), list(weapon_weights.values())).copy()

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
        quality = random.choices(list(qualities.keys()), list(quality_weights.values())).copy()
        item_base.apply_quality(quality)

    if random.random() <= effect_prob
        effect = random.choices(list(effects.keys()), list(effect_weights.values())).copy()
        apply_effect(item_base, effect)

    format_name(item_base)
    components = {
        "Item": Item(item_base['functions'], item_base['uses'], item_base['type'], item['equip_abilities'], item_base['kwargs'])
    }

    return Entity(x, y, item_base['icon'], item_base['color'], item_base['name'], blocks=False, render_order=RenderOrder.ITEM, message_log=log, state=AIStates.INANIMATE, components=components))


def apply_effect(item, effect_name):
    effect_description_obj = effects[effect_name]
    item['equip_abilities'] = [...item['equip_abilities'], item_function_dict[effect_name]]
    item['effect_description'] = effect_description_obj['description']
    item['effect_name'] = effect_description_obj['name']
    item['kwargs'] = {...item['kwargs'], ...effect_description_obj['kwargs']}
    

def apply_quality(item, quality_name):
    quality_description_obj = qualities[quality_name]
    item['functions'] = [...item['functions'], item_equip_dict[quality_name]]
    item['quality_description'] = quality_description_obj['description']
    item['quality_name'] = quality_description_obj['name']
    item['kwargs'] = {...item['kwargs'], ...quality_description_obj['kwargs']}

def format_name(item):
    item_name = item['name'].format(item['quality_name'] if 'quality_name' in item else '', item['effect_name'] if 'effect_name' in item else '')
    item['description'] = item['description'].format(item['quality_description'] if 'quality_description' in item else '', item['effect_description'] if 'effect_description' in item else '')

