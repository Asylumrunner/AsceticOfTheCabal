from game_states import AIStates
from game_constants import npcs, items
from collections import OrderedDict
from components.item import ItemType

# A collection of conditionals which are used to inspect entities in the game and give vague readouts to the UI
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
    elif fighter.hp == 0:
        description_text['hurt'] = "It lies on the ground, dead"
    
    return description_text


def inspect_item(entity, desc):
    description_text = desc
    item = entity.get_component("Item")

    description_text['description'] = item.description

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
        description_text['description'] = npcs[entity.base_name]['description']
        description_text = inspect_fighter(entity, description_text)
        description_text['hostile'] = "It does not appear hostile to you" if entity.state == AIStates.FRIENDLY else "It looks hostile"
    elif entity.has_component("Item"):
        description_text = inspect_item(entity, description_text)

    return list(description_text.values())

def inspect_player_status(player):
    description_text = OrderedDict()

    fighter = player.get_component("Fighter")
    inventory = player.get_component("Inventory")
    devotee = player.get_component("Devotee")
    statuses = player.get_component("StatusContainer")

    description_text['health'] = "{} of {} HP".format(fighter.hp, fighter.max_hp)
    description_text['defense'] = "{} Defense".format(fighter.get_defense())
    description_text['money'] = "${} in wallet".format(fighter.money)
    status_list = statuses.get_statuses()
    description_text['statuses'] = "Currently {}".format(", ".join(status_list)) if status_list else "No status effects"
    
    description_text['gap_1'] = "        ---        "

    description_text ['unarmed_power'] = "Unarmed attacks deal {} damage".format(fighter.power)
    description_text ['armed_power'] = "Melee attacks deal {} damage".format(fighter.get_modified_strength())

    description_text['gap_2'] = "        ---        "

    description_text['devotion'] = "{} of {} Devotion".format(devotee.curr_devotion, devotee.max_devotion)
    description_text['god'] = "Devoted to {}".format(devotee.get_god().name)

    description_text['gap_3'] = "        ---        "

    description_text['capacity'] = "{} of {} inventory slots filled".format(len(inventory.items), inventory.capacity)

    return list(description_text.values())

