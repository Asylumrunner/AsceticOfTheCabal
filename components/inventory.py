import tcod as libtcod
from .item import ItemType
from game_messages import Message

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

    def add_item(self, item):
        if len(self.items) >= self.capacity:
            self.owner.log.add_message(Message("Your inventory is full! Cannot pick up any more items", libtcod.yellow))
        else:
            self.items.append(item)
            self.owner.log.add_message(Message("Picked up {0}".format(item.name), libtcod.green))
    
    def remove_item(self, item):
        try:
            self.items.remove(item)
            self.owner.log.add_message(Message("{0} broke!".format(item.name), libtcod.red))
        except:
            print("Item not found")
    
    def equip_item(self, item):
        try:
            item_type = ItemType(item.get_component("Item").item_type)
            if item_type.name != 'NONE':
                last_item = self.equipped[item_type.name]
                if last_item is not item:
                    self.equipped[item_type.name] = item
                    item.get_component("Item").equip(player=self.owner)
                    self.owner.log.add_message(Message("Equipped {0}".format(item.name), libtcod.green))
                    self.items = [inv_item for inv_item in self.items if inv_item is not item]
                    if(last_item):
                        last_item.get_component("Item").unequip(player=self.owner)
                        self.owner.log.add_message(Message("Unequipped {0}".format(last_item.name), libtcod.green))
                        self.items.append(last_item)
            self.calculate_armor()

        except Exception as e:
            print("Equipping exception: {}".format(e))

    def slot_filled(self, slot_name):
        return True if slot_name in self.equipped and self.equipped[slot_name] != None else False
    
    def get_slot(self, slot_name):
        return self.equipped[slot_name]

    def calculate_armor(self):
        armor_value = 0
        for slot, item in self.equipped.items():
            if item and item.get_component("Item").function_kwargs and item.get_component("Item").function_kwargs['armor']:
                armor_value += item.get_component("Item").function_kwargs['armor']
        self.owner.get_component("Fighter").change_defense(armor_value)
