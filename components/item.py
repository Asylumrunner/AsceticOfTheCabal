from enum import Enum

class ItemType(Enum):
    NONE = 0
    HEAD = 1
    BODY = 2
    LEGS = 3
    TRINKET = 4
    MELEE = 5
    RANGED = 6

class Item:
    def __init__(self, use_function=None, uses=-99, item_type=ItemType.NONE, **kwargs):
        self.use_function = use_function
        self.uses = uses
        self.function_kwargs = kwargs
        self.item_type = item_type
    
    def use(self, *args):
        for function in self.use_function:
            function(*args, **self.function_kwargs)
        
        if self.uses != -99:
            self.uses -= 1
            if self.uses <= 0:
                return True
        
        return False

    