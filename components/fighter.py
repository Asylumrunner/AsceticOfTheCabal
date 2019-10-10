class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
    
    def take_damage(self, damage):
        results = []
        self.hp -= damage

        if self.hp <= 0:
            results.append({'dead': self.owner})
        
        return results
    
    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.extend(target.fighter.take_damage(damage))
            results.append({'message': '{0} attacks {1}, dealing {2} damage'.format(self.owner.name.capitalize(), target.name.capitalize(), damage)})
        else:
            results.append({'message': 'Get absolutely rekt, {0}, {1}\'s armor is too strong and repels your attack'.format(self.owner.name.capitalize(), target.name.capitalize())})

        return results
    