
# A class used to hold Devotion, the resource used to cast Cabal spells
# Still very much under construction as the Cabal systems are implemented
class Devotee:
    def __init__(self, max_devotion):
        self.max_devotion = max_devotion
        self.curr_devotion = max_devotion
    
    #add the given modifier to current devotion, using 0 and max_devotion as bounds
    def modify_devotion(self, devotion):
        self.curr_devotion = max(0, min(curr_devotion+devotion, max_devotion))