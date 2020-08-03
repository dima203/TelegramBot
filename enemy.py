from calculating import calculate_armor
from random import randint
import math


class Enemy:
    def __init__(self):
        self.level = 0
        self.health = 0
        self.damage = 0
        self.armor = 0
        self.exp = 0

    def info(self):
        string = f'''Здоровье: {self.health}
Атака: {self.damage}
Броня: {self.armor}'''
        return string

    def attack(self, damage):
        self.health -= damage * (1 - calculate_armor(self.armor))

    def get_exp(self, player_level):
        exp = randint(self.exp - 5, self.exp + 5)
        x = player_level - self.level + 1
        return round(-math.log(x, 1.1) + exp)


class Goblin(Enemy):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.health = 50
        self.damage = 3
        self.armor = 0
        self.exp = 50
