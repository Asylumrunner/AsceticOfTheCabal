# A one-stop compendium of all qualities (consant buff/debuffs) an item may possess

class Heresy:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    def equip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").add_faction(2)
    def unequip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").remove_faction(2)

class Armor:
    def __init__(self, **kwargs):
        self.armor_value = kwargs['armor'] if 'armor' in kwargs else 0
    def equip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_defense(self.armor_value)
    def unequip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_defense(self.armor_value * -1)

class MaxHealthUp:
    def __init__(self, **kwargs):
        self.health_buff = kwargs["health_up"] if "health_up" in kwargs else 0
    def equip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_max_hp(self.health_buff)
    def unequip(self, *args, **kwargs):
        if "player" in kwargs:
            kwargs['player'].get_component("Fighter").change_max_hp(self.health_buff * -1)

item_equip_dict = {
    "Armor": Armor,
    "Max_Health_Up": MaxHealthUp,
    "Heretical": Heresy
}

qualities = {
    "Max_Health_Up": {
        "description": "soothing ",
        "name": "Invigorating ",
        "kwargs": {
            "health_up": 30
        },
        'targets': [1, 2, 3, 4, 5, 6],
        'effects': ["Max_Health_Up"]
    },
    "Heretical": {
        "description": "heretical ",
        "name": "Heretical ",
        "kwargs": {

        },
        'targets': [1, 2, 3, 4, 5, 6],
        'effects': ["Heretical"]
    }
}

quality_weights = [1, 1000]