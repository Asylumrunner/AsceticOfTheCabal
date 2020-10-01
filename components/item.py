from enum import Enum
from components.weapon import Weapon

class ItemType(Enum):
    NONE = 0
    HEAD = 1
    BODY = 2
    LEGS = 3
    TRINKET = 4
    MELEE = 5
    RANGED = 6

class Item:
    def __init__(self, use_function=None, uses=-99, item_type=ItemType.NONE, equip_effects=None, strength=0, **kwargs):
        self.use_function = use_function
        self.uses = uses
        self.function_kwargs = kwargs
        self.item_type = item_type
        self.equip_effects = equip_effects

        if strength != 0:
            self.weapon = Weapon(strength)
        else:
            self.weapon = None
    
    def equip(self, **kwargs):
        print("Equip called on Item")
        for effect in self.equip_effects:
            effect.equip(**kwargs)

    def unequip(self, **kwargs):
        for effect in self.equip_effects:
            effect.unequip(**kwargs)
    
    def use(self, *args):
        print(self.use_function)
        for function in self.use_function:
            function(args, self.function_kwargs)
        
        if self.uses != -99:
            self.uses -= 1
            if self.uses <= 0:
                return True
        
        return False

    