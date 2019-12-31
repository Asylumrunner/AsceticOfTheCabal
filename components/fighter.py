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
        damage = self.power - target.fighter.defense
        if damage > 0:
            target.fighter.take_damage(damage)
            self.owner.log.add_message(Message('{0} attacks {1}, dealing {2} damage'.format(self.owner.name.capitalize(), target.name.capitalize(), damage), libtcod.white))
        else:
            self.owner.log.add_message(Message('Get absolutely rekt, {0}, {1}\'s armor is too strong and repels your attack'.format(self.owner.name.capitalize(), target.name.capitalize()), libtcod.white))

    def isAlive(self):
        return self.hp > 0

    def die(self):
        self.owner.log.add_message(Message('{0} is dead!'.format(self.owner.name.capitalize()), libtcod.orange))
        self.owner.char = '%'
        self.owner.color = libtcod.dark_red

        self.owner.blocks = False
        self.owner.ai = None
        self.owner.render_order = RenderOrder.CORPSE
        self.owner.name = 'remains of {0}'.format(self.owner.name.capitalize())

        return Entity(self.owner.x, self.owner.y, '$', libtcod.green, "${}".format(self.money), blocks=False, render_order=RenderOrder.ITEM, fighter=None, ai=None, item=None, inventory=None, message_log=self.owner.log, state=AIStates.INANIMATE, money=Money(self.money)) if self.money > 0 else None
    
    def pick_up_money(self, money_obj):
        if money_obj.money:
            self.money += money_obj.money.value