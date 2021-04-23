from enum import Enum
#from god_abilities import abilities

class CabalGods(Enum):
    MERCURIAL_CALAMITY = 1
    XALAN_NORE = 2
    OBLIVION = 3
    LEGIONOUS_PARABELLICA = 4
    PARAGONOTH = 5
    MISTER_VIVISECT = 6
    CHRYSANTHEMUM_OF_THE_COLDEST_COLD = 7

# A class used to hold Devotion, the resource used to cast Cabal spells
# Still very much under construction as the Cabal systems are implemented
class Devotee:
    def __init__(self, max_devotion, god=CabalGods.MERCURIAL_CALAMITY):
        self.max_devotion = max_devotion
        self.curr_devotion = max_devotion
        self.god = god
    
    #add the given modifier to current devotion, using 0 and max_devotion as bounds
    def modify_devotion(self, devotion):
        self.curr_devotion = max(0, min(curr_devotion+devotion, max_devotion))
    
    def get_god(self):
        return self.god

    def god_ability(self):
        #if(curr_devotion >= abilities[self.god]['cost']):
        #    abilities[self.god]['function'](self.owner)
        #    curr_devotion = curr_devotion - abilities[self.god]['cost']
        return True