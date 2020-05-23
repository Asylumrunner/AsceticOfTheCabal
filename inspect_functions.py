from game_states import AIStates
from game_constants import npcs, items
from collections import OrderedDict
from components.item import ItemType

def inspect_fighter(entity, desc):
    description_text = desc
    fighter = entity.get_component("Fighter")

    if fighter.max_hp > 50:
        description_text['max_hp'] = "It looks divine in strength"
    elif fighter.max_hp > 40:
        description_text['max_hp'] = "It looks like a serious threat"
    elif fighter.max_hp > 30:
        description_text['max_hp'] = "It looks like it can take a real beating"
    elif fighter.max_hp > 20:
        description_text['max_hp'] = "It looks like it will put up a fight"
    elif fighter.max_hp > 10:
        description_text['max_hp'] = "It looks like a moderate threat"
    else:
        description_text['max_hp'] = "It is a common pest"

    if fighter.hp/fighter.max_hp == 1:
        description_text['hurt'] = "It looks completely healthy"
    elif fighter.hp/fighter.max_hp >= 0.5:
        description_text['hurt'] = "It's been bruised up a little"
    elif fighter.hp/fighter.max_hp >= 0.1:
        description_text['hurt'] = "It's bloodied with wounds of battle"
    elif fighter.hp/fighter.max_hp > 0:
        description_text['hurt'] = "It's on death's door"
    
    return description_text

def inspect_item(entity, desc):
    description_text = desc
    item = entity.get_component("Item")

    if item.item_type == ItemType.BODY.value:
        description_text['item_type'] = "It looks like it's worn on the Body"
    elif item.item_type == ItemType.HEAD.value:
        description_text['item_type'] = "It looks like it's worn on the Head"
    elif item.item_type == ItemType.LEGS.value:
        description_text['item_type'] = "It looks like it's worn on the Legs"
    elif item.item_type == ItemType.MELEE.value:
        description_text['item_type'] = "It looks like a Melee weapon"
    elif item.item_type == ItemType.RANGED.value:
        description_text['item_type'] = "It looks like a Ranged weapon"
    elif item.item_type == ItemType.TRINKET.value:
        description_text['item_type'] = "It looks like some kind of Trinket"
    
    return description_text

def inspect_entity(entity):
    description_text = OrderedDict()

    if entity.has_component("Fighter"):
        description_text['description'] = npcs[entity.name]['description']
        description_text = inspect_fighter(entity, description_text)
        description_text['hostile'] = "It does not appear hostile to you" if entity.state == AIStates.FRIENDLY else "It looks hostile"
    elif entity.has_component("Item"):
        description_text['description'] = items[entity.name]['description']
        description_text = inspect_item(entity, description_text)

    return list(description_text.values())