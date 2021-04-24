import random
from entity import Entity
from .components.item import Item
from render_functions import RenderOrder
from game_states import AIStates


class Shop():
    def __init__(self, items, description):
        self.stock = []
        for x in range(3):
            item_data = random.choice(items)
            components = {
                'Item': Item(item_data['functions'], item_data['uses'], item_data['type'], item_data['equip_abilities'], item_base['strength'], item_base['strength'], item_base['defense'], **item_base['kwargs'])
            }
            self.stock.append(Entity(owner.x, owner.y, item_data['icon'], item_data['color'], item_data['name'], False, RenderOrder.ITEM, log, state=AIStates.INANIMATE, components=components))
        self.description = description

    def purchase(self, selection, player):
        if player.get_component("Fighter").money >= self.stock[selection].price:
            player.get_component("Fighter").money -= self.stock[selection].price
            player.get_component("Inventory").add_item(self.stock.pop(selection))
