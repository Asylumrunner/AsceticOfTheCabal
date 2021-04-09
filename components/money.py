import tcod as libtcod

# A class for a unit of monetary value
# Pretty much does nothing other than store value
class Money():
    def __init__(self, value):
        self.value = value