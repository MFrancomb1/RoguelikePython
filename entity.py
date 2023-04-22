from typing import Tuple

class Entity:
    #Object representing players, enemies, items, etc.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char= char
        self.color = color

    def move(self, dx, dy):\
        # move the entity by (dx, dy) spaces
        self.x += dx
        self.y += dy