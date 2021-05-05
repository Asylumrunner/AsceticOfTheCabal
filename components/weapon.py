# an add-on class added to Items that can be used to deal damage 
class Weapon:
    def __init__(self, strength=1, ammo=0):
        self.strength = strength
        self.ammo = ammo