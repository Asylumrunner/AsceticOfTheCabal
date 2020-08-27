import tcod as libtcod
from game_messages import Message
from render_functions import RenderOrder
from game_states import AIStates
from entity import Entity
from components.money import Money

class Fighter:
    def __init__(self, hp, defense, power, money=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.money = money
    
    def take_damage(self, damage):
        self.hp -= damage
    
    def attack(self, target):
        damage = self.power - target.get_component("Fighter").defense
        if damage > 0:
            target.get_component("Fighter").take_damage(damage)
            self.owner.log.add_message(Message('{0} attacks {1}, dealing {2} damage'.format(self.owner.name.capitalize(), target.name.capitalize(), damage), libtcod.white))
            if self.owner.has_component("Inventory") and self.owner.get_component("Inventory").slot_filled("WEAPON"):
                weapon = self.owner.get_component("Inventory").get_slot("WEAPON")
                weapon.get_component("Item").use(self.owner, target)
        else:
            self.owner.log.add_message(Message('Get absolutely rekt, {0}, {1}\'s armor is too strong and repels your attack'.format(self.owner.name.capitalize(), target.name.capitalize()), libtcod.white))

    def isAlive(self):
        return self.hp > 0

    def die(self):
        self.owner.log.add_message(Message('{0} is dead!'.format(self.owner.name.capitalize()), libtcod.orange))
        self.owner.char = '%'
        self.owner.color = libtcod.dark_red

        self.owner.blocks = False
        del self.owner.components['AI']
        self.owner.render_order = RenderOrder.CORPSE
        self.owner.name = 'remains of {0}'.format(self.owner.name.capitalize())

        money_components = {
            "Money": Money(self.money)
        }
        return Entity(self.owner.x, self.owner.y, '$', libtcod.green, "${}".format(self.money), blocks=False, render_order=RenderOrder.ITEM, message_log=self.owner.log, state=AIStates.INANIMATE, components=money_components) if self.money > 0 else None
    
    def pick_up_money(self, money_obj):
        if money_obj.has_component("Money"):
            self.money += money_obj.get_component("Money").value
    
    def change_defense(self, defense_value):
        self.defense += defense_value
        print("Current health of {} is {}".format(self.owner.name, self.defense))
    
    def change_max_hp(self, hp_modification):
        self.max_hp += hp_modification
        print("Current maximum HP of {} is {}".format(self.owner.name, self.max_hp))