from enum import Enum
from components.weapon import Weapon
from components.armor import Armor

class ItemType(Enum):
    NONE = 0
    HEAD = 1
    BODY = 2
    LEGS = 3
    TRINKET = 4
    MELEE = 5
    RANGED = 6

# A class that serves as an abstraction for every item and the numerous effects they might possess
# This gets _preeeeeetty abstracted_

class Item:
    def __init__(self, use_function=None, uses=-99, item_type=ItemType.NONE, equip_effects=None, strength=0, defense=0, **kwargs):
        self.use_function = use_function
        self.uses = uses
        self.function_kwargs = kwargs
        self.item_type = item_type
        self.equip_effects = equip_effects

        if strength != 0:
            self.weapon = Weapon(strength)
        else:
            self.weapon = None

        if defense != 0:
            self.armor = Armor(defense)
        else:
            self.armor = None
    
    # Trigger all existing equip effects, passing in a generic list of kwargs
    def equip(self, **kwargs):
        print("Equip called on Item")
        for effect in self.equip_effects:
            effect.equip(**kwargs)

    # Trigger all existing unequip effects, passing in a generic list of kwargs
    def unequip(self, **kwargs):
        for effect in self.equip_effects:
            effect.unequip(**kwargs)
    
    # Use the item one time, calling every use function and passing in the function_kwargs set at init as well as any args given now
    # if the item has limited uses, tick those uses down one and return if it needs to be destroyed
    def use(self, *args):
        print(self.use_function)
        for function in self.use_function:
            print("Use function:")
            print(args)
            function(*args, **self.function_kwargs)
        
        if self.uses != -99:
            self.uses -= 1
            if self.uses <= 0:
                return True
        
        return False

    