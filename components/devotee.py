
class Devotee:
    def __init__(self, max_devotion):
        self.max_devotion = max_devotion
        self.curr_devotion = max_devotion
    
    def modify_devotion(self, devotion):
        self.curr_devotion = max(0, min(curr_devotion+devotion, max_devotion))