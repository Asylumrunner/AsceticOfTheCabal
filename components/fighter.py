import tcod as libtcod
from game_messages import Message
from render_functions import RenderOrder
from game_states import AIStates
from entity import Entity
from components.money import Money

# A beefy boy of a class, representing anything that can fight

class Fighter:
    def __init__(self, hp, defense, power, money=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.money = money
    
    # Decrement HP by the given amount
    def take_damage(self, damage):
        self.hp -= damage
    
    # The basic logic for inflicting damage on another target
    def attack(self, target):
        # If you have an inventory, check if you have a melee weapon, and if so use that weapon's damage, otherwise use character strength, reduce by target armor, and deal damage
        # The weird conditional is because something in the MELEE slopt might not be a weapon, and if so it shouldn't be used for damage 
        if self.owner.has_component("Inventory"):
            eq_weapon = self.owner.get_component("Inventory").get_slot("MELEE")
            unblocked_damage = eq_weapon.get_component("Item").weapon.strength if eq_weapon and eq_weapon.get_component("Item").weapon != None else self.power
            damage = unblocked_damage - target.get_component("Fighter").get_defense()

            #Activate any effects of the Melee item against the target (e.g enchantments)
            if eq_weapon:
                eq_weapon.get_component("Item").use(self.owner, target)
        
        # if you don't have any weapons, just punchem
        else:
            damage = self.power - target.get_component("Fighter").get_defense()

        # if you successfully dealt any damage, inflict that damage on the target, and write a UI message
        if damage > 0:
            target.get_component("Fighter").take_damage(damage)
            self.owner.log.add_message(Message('{0} attacks {1}, dealing {2} damage'.format(self.owner.name.capitalize(), target.name.capitalize(), damage), libtcod.white))
            #TODO: what the fuck does this do?
            if self.owner.has_component("Inventory") and self.owner.get_component("Inventory").slot_filled("WEAPON"):
                weapon = self.owner.get_component("Inventory").get_slot("WEAPON")
                weapon.get_component("Item").use(self.owner, target)
        else:
            self.owner.log.add_message(Message('Get absolutely rekt, {0}, {1}\'s armor is too strong and repels your attack'.format(self.owner.name.capitalize(), target.name.capitalize()), libtcod.white))

    # return a boolean value if you have at least 1 HP
    def isAlive(self):
        return self.hp > 0

    # function invoked by cleanup code to kill enemies
    def die(self):
        # write a death message to the log, change the sprite to a dead body
        self.owner.log.add_message(Message('{0} is dead!'.format(self.owner.name.capitalize()), libtcod.orange))
        self.owner.char = '%'
        self.owner.color = libtcod.dark_red

        # make the corpse intangible, remove its AI, move it to the bottom of the render order, and change it name to a corpse
        self.owner.blocks = False
        del self.owner.components['AI']
        self.owner.render_order = RenderOrder.CORPSE
        self.owner.name = 'remains of {0}'.format(self.owner.name.capitalize())

        #if you had any scratch on you, spawn a Money object in-world for the player to pick up
        money_components = {
            "Money": Money(self.money)
        }
        return Entity(self.owner.x, self.owner.y, '$', libtcod.green, "${}".format(self.money), blocks=False, render_order=RenderOrder.ITEM, message_log=self.owner.log, state=AIStates.INANIMATE, components=money_components) if self.money > 0 else None
    
    # takes a money object that the Fighter is over and grab it
    def pick_up_money(self, money_obj):
        if money_obj.has_component("Money"):
            self.money += money_obj.get_component("Money").value
    
    # gets the total defensive value (inherit defense + armor) of a character
    def get_defense(self):
        if self.owner.has_component("Inventory"):
            return self.defense + self.owner.get_component("Inventory").calculate_armor()
        else:
            return self.defense

    # changes the defense to a given number
    def change_defense(self, defense_value):
        self.defense = defense_value
        print("Current defense of {} is {}".format(self.owner.name, self.defense))
    
    # modify your max HP with a given number, NOT changing current HP
    def change_max_hp(self, hp_modification):
        self.max_hp += hp_modification
        print("Current maximum HP of {} is {}".format(self.owner.name, self.max_hp))

    #TODO: Fighters that drop an inventory should drop all their shit too