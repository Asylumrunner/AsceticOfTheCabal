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
        item_type = ItemType(item.get_component("Item").item_type)
        try:
            last_item = self.equipped[item_type.name]
            if(last_item is not item):
                self.equipped[item_type.name] = item
                item.get_component("Item").equip(player=self.owner)
                self.owner.log.add_message(Message("Equipped {0}".format(item.name), libtcod.green))
                self.items = [inv_item for inv_item in self.items if inv_item is not item]
                if(last_item):
                    item.get_component("Item").unequip(player=self.owner)
                    self.owner.log.add_message(Message("Unequipped {0}".format(last_item.name), libtcod.green))
                    self.items.append(last_item)
        except Exception as e:
            print("Equipping exception: {}".format(e))
