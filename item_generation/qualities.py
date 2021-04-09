# A one-stop compendium of all qualities (consant buff/debuffs) an item may possess

class Armor:
    def __init__(self, **kwargs):
        self.armor_value = kwargs['armor'] if 'armor' in kwargs else 0
        print("Armor initialized with an armor value of {}".format(self.armor_value))
    def equip(self, *args, **kwargs):
        print("Equip called on the Armor attribute")
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_defense(self.armor_value)
    def unequip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_defense(self.armor_value * -1)

class MaxHealthUp:
    def __init__(self, **kwargs):
        self.health_buff = kwargs["health_up"] if "health_up" in kwargs else 0
    def equip(self, *args, **kwargs):
        print("Equip called on the MaxHealthUp attribute")
        print(kwargs)
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_max_hp(self.health_buff)
    def unequip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_max_hp(self.health_buff * -1)

item_equip_dict = {
    "Armor": Armor,
    "Max_Health_Up": MaxHealthUp
}

qualities = {
    "Max_Health_Up": {
        "description": " that emanates a soothing sensation which melts into your skin",
        "name": "Restorative ",
        "kwargs": {
            "health_up": 30
        },
        'targets': [1, 2, 3, 4, 5, 6],
        'effects': ["Max_Health_Up"]
    }
    
}

quality_weights = [1]