import tcod as libtcod
from item import ItemType
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
        item_type = item.item_type
        something_equipped = True
        if item_type == ItemType.HEAD:
            last_item = self.equipped['HEAD']
            self.equipped['HEAD'] = item
        elif if item_type == ItemType.BODY:
            last_item = self.equipped['BODY']
            self.equipped['BODY'] = item
        elif if item_type == ItemType.LEGS:
            last_item = self.equipped['LEGS']
            self.equipped['LEGS'] = item
        elif if item_type == ItemType.TRINKET:
            last_item = self.equipped['TRINKET']
            self.equipped['TRINKET'] = item
        elif if item_type == ItemType.MELEE:
            last_item = self.equipped['MELEE']
            self.equipped['MELEE'] = item
        elif if item_type == ItemType.RANGED:
            last_item = self.equipped['RANGED']
            self.equipped['RANGED'] = item
        else:
            something_equipped = False
        
        if(something_equipped):
            self.owner.log.add_message(Message("Equipped {0}".format(item.name), libtcod.green))
            if(last_item):
                self.owner.log.add_message(Message("Unequipped {0}".format(last_item.name), libtcod.green))
