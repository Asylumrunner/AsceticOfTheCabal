import tcod as libtcod
from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

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