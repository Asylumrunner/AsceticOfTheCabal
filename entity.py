class Entity:
    
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, x, y):
        self.x += x
        self.y += y