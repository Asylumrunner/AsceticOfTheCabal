from .base_items import weapons, armor, potions, weapon_weights, armor_weights, potion_weights, starting_pistol
from .qualities  import qualities, quality_weights, item_equip_dict
from .item_functions import item_function_dict, effects, effect_weights
from components.item import Item
from entity import Entity
from render_functions import RenderOrder
from game_states import AIStates
import game_constants
import random
import pprint

# A collection of the functions used to randomly generate a weapon or armor

def generate_armor(quality_prob, effect_prob, x, y, log):
    #pick a base item from base_items using the appropriate probability weights
    item_base = armor[random.choices(list(armor.keys()), armor_weights)[0]].copy()
    if 'kwargs' not in item_base:
        item_base['kwargs'] = {}

    # If the item base has any qualities (why the fuck am I calling them equip abilities that is deeply confusing), add them to the item
    if 'equip_abilities' not in item_base:
        item_base['equip_abilities'] = []
    else:
        item_base['equip_abilities'] = [item_equip_dict[quality] for quality in item_base['equip_abilities']]

    # if the item has any on-use abilities, add them to the item
    if 'functions' not in item_base:
        item_base['functions'] = []
    else:
        item_base['functions'] = [item_function_dict[effect] for effect in item_base['functions']]

    # randomly determine if the item will get a quality, which is randomly chose and applied to the item
    if random.random() <= quality_prob:
        tries = 5
        while tries > 0:
            quality = qualities[random.choices(list(qualities.keys()), quality_weights)[0]].copy()
            if item_base['type'] in quality['targets']:
                apply_quality(item_base, quality)
                break
            else:
                tries -= 1

    # randomly determine if the item will get an on-use ability, which is randomly chosen and applied to the item
    if random.random() <= effect_prob:
        tries = 5
        while tries > 0:
            effect = effects[random.choices(list(effects.keys()), effect_weights)[0]].copy()
            if item_base['type'] in effect['targets']:
                apply_effect(item_base, effect)
                break
            else:
                tries -= 1

    # set the item's name to reflect any qualities or on-use abilities it has
    format_name(item_base)

    # generate an Entity object for the item
    components = {
        "Item": Item(use_function=item_base['functions'], uses=item_base['uses'], item_type=item_base['type'], equip_effects=item_base['equip_abilities'], strength=0, defense=item_base['defense'], price = item_base['price'], description = item_base['description'], **item_base['kwargs'])
    }
    
    return Entity(x, y, item_base['icon'], item_base['color'], item_base['name'], blocks=False, render_order=RenderOrder.ITEM, message_log=log, state=AIStates.INANIMATE, components=components)


def generate_weapon(quality_prob, effect_prob, x, y, log):
    # Pick a base item from base_items using the appropriate probability weights
    item_base = weapons[random.choices(list(weapons.keys()), weapon_weights)[0]].copy()
    if 'kwargs' not in item_base:
        item_base['kwargs'] = {}

    # If the item base has any qualities (why the fuck am I calling them equip abilities that is deeply confusing), add them to the item
    if 'equip_abilities' not in item_base:
        item_base['equip_abilities'] = []
    else:
        item_base['equip_abilities'] = [item_equip_dict[quality] for quality in item_base['equip_abilities']]

    # if the item has any on-use abilities, add them to the item
    if 'functions' not in item_base:
        item_base['functions'] = []
    else:
        item_base['functions'] = [item_function_dict[effect] for effect in item_base['functions']]

    # randomly determine if the item will get a quality, which is randomly chose and applied to the item
    #if random.random() <= quality_prob:
    if True:
        while True:
            quality = qualities[random.choices(list(qualities.keys()), quality_weights)[0]].copy()
            if item_base['type'] in quality['targets']:
                break
        apply_quality(item_base, quality)

    # randomly determine if the item will get an on-use ability, which is randomly chosen and applied to the item
    if random.random() <= effect_prob:
        while True:
            effect = effects[random.choices(list(effects.keys()), effect_weights)[0]].copy()
            if item_base['type'] in effect['targets']:
                break
        apply_effect(item_base, effect)

    # set the item's name to reflect any qualities or on-use abilities it has
    format_name(item_base)

    # generate an Entity object for the item
    components = {
        "Item": Item(use_function=item_base['functions'], uses=item_base['uses'], item_type=item_base['type'], equip_effects=item_base['equip_abilities'], strength=item_base['strength'], defense=0, price = item_base['price'], description = item_base['description'], **item_base['kwargs'])
    }

    item = Entity(x, y, item_base['icon'], item_base['color'], item_base['name'], blocks=False, render_order=RenderOrder.ITEM, message_log=log, state=AIStates.INANIMATE, components=components)
    return item

def generate_potion(x, y, log):
    item_base = potions[random.choices(list(potions.keys()), potion_weights)[0]].copy()
    
    while True:
            effect = effects[random.choices(list(effects.keys()), effect_weights)[0]].copy()
            if item_base['type'] in effect['targets']:
                break
    apply_effect(item_base, effect)

    format_potion(item_base, effect)
    
    components = {
        "Item": Item(use_function=item_base['functions'], uses=item_base['uses'], item_type=item_base['type'], equip_effects=item_base['equip_abilities'], strength=item_base['strength'], defense=0, price = item_base['price'], description = item_base['description'], **item_base['kwargs'])
    }
    item = Entity(x, y, item_base['icon'], item_base['color'], item_base['name'], blocks=False, render_order=RenderOrder.ITEM, message_log=log, state=AIStates.INANIMATE, components=components)
    return item

def apply_effect(item, effect):
    # if an effect is to be applied, add it, its name, its description, and its kwargs to the item
    item['functions'] = item['functions'] + [item_function_dict[func] for func in effect['hit_effect']]
    item['effect_description'] = effect['description']
    item['effect_name'] = effect['name']
    item['kwargs'] = {**item['kwargs'], **effect['kwargs']}

def apply_quality(item, quality):
    # if a quality is to be applied, add it, its name, its description, and its kwargs to the item
    item['equip_abilities'] = item['equip_abilities'] + [item_equip_dict[effect](**quality['kwargs']) for effect in quality['effects']]
    item['quality_description'] = quality['description']
    item['quality_name'] = quality['name']
    item['kwargs'] = {**item['kwargs'], **quality['kwargs']}

def format_name(item):
    # compound together all details of an item into a complete description and name
    item['name'] = item['name'].format(item['quality_name'] if 'quality_name' in item else '', item['effect_name'] if 'effect_name' in item else '')
    item['description'] = item['description'].format(item['quality_description'] if 'quality_description' in item else '', item['effect_description'] if 'effect_description' in item else '')

def format_potion(item, effect):
    item['name'] = item['name'].format(item['effect_name'])
    item['description'] = item['description'].format(effect['potion_color_name'])
    item['color'] = effect['potion_color'] if 'potion_color' in effect else item['color']

def generate_starting_pistol(log):
    # sort of a weird one, this function puts together the Ascetic's Pistol that every run begins with
    components = {
        'Item': Item(use_function=starting_pistol['functions'], uses=starting_pistol['uses'], item_type=starting_pistol['type'], equip_effects=starting_pistol['equip_abilities'], strength=starting_pistol['strength'], defense=0, price=starting_pistol['price'], **starting_pistol['kwargs'])
    }

    gun = Entity(0, 0, starting_pistol['icon'], starting_pistol['color'], starting_pistol['name'], blocks=False, render_order=RenderOrder.ITEM, message_log=log, state=AIStates.INANIMATE, components=components)

    return gun