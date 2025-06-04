import random

class Dice:
    def __init__(self):
        self.dice1 = 0
        self.dice2 = 0

    def roll(self):
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        
    @property
    def total(self):
        return self.dice1 + self.dice2

    @property
    def is_dubel(self):
        return self.dice1 == self.dice2
    