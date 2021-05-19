import tcod as libtcod
from .item import ItemType
from game_messages import Message

# The holder class that keeps track of all of the shit a character has picked up

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
        self.equipped = {
            'HEAD': None,
            'BODY': None,
            'LEGS': None,
            'TRINKET': None,
            'MELEE': None,
            'RANGED': None
        }

    # Adds an item object to the items list, provided the player has capacity
    def add_item(self, item):
        if len(self.items) >= self.capacity:
            self.owner.log.add_message(Message("Your inventory is full! Cannot pick up any more items", libtcod.yellow))
        else:
            self.items.append(item)
            self.owner.log.add_message(Message("Picked up {0}".format(item.name), libtcod.green))
    
    # removes an item from the player's inventory. Currently written with breaking/expenditure as main use-case
    # can probably be used for dropping itmes too
    def remove_item(self, item):
        try:
            self.items.remove(item)
            self.owner.log.add_message(Message("{0} broke!".format(item.name), libtcod.red))
        except:
            print("Item not found")
    
    # equip an item to the appropriate slot
    def equip_item(self, item):
        try:
            # determines what the type of the item is (item_type is an enum)
            item_type = ItemType(item.get_component("Item").item_type)
            if item_type.name != 'NONE':
                # if the item you're trying to equip isn't the item you currently have in the corresponding slot
                last_item = self.equipped[item_type.name]
                if last_item is not item:
                    #equip the item, adding it to the equip dict and triggering any on-equip effects
                    self.equipped[item_type.name] = item
                    item.get_component("Item").equip(player=self.owner)
                    self.owner.log.add_message(Message("Equipped {0}".format(item.name), libtcod.green))
                    # remove the item from your inventory (this feels like a bad way to do this)
                    self.items = [inv_item for inv_item in self.items if inv_item is not item]
                    # if you replaced something in that slot, unequip it and add it back to your regular inventory
                    if(last_item):
                        last_item.get_component("Item").unequip(player=self.owner)
                        self.owner.log.add_message(Message("Unequipped {0}".format(last_item.name), libtcod.green))
                        self.items.append(last_item)
            # recalculate armor value
            self.calculate_armor()

        except Exception as e:
            print("Equipping exception: {}".format(e))

    def unequip_slot(self, slot_name):
        if not self.slot_filled(slot_name.name):
            return False
        else:
            equipped_item = self.get_slot(slot_name.name)
            equipped_item.get_component("Item").unequip(player=self.owner)
            self.owner.log.add_message(Message("Unequipped {0}".format(equipped_item.name), libtcod.green))
            self.items.append(equipped_item)
            self.equipped[slot_name.name] = None
            return True

    # returns true if there is a not-None item in the slot
    def slot_filled(self, slot_name):
        return True if slot_name in self.equipped and self.equipped[slot_name] != None else False
    
    # returns whatever the item is in the described slot (including, potentially, None)
    def get_slot(self, slot_name):
        return self.equipped[slot_name]

    # iterate through every item equipped, check if it's armor, and if so, add it's armor value to a running sum that is then set as the character's defense
    def calculate_armor(self):
        armor_value = 0
        for slot, item in self.equipped.items():
            if item and item.get_component("Item").armor:
                armor_value += item.get_component("Item").armor.armor_value
        return armor_value
