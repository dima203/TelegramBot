from calculating import calculate_armor
from random import randint
import math
import inline_keyboards as ikb


# Родительский класс всех мобов
class Enemy:
    def __init__(self):
        self.level = 0
        self.health = 0
        self.damage = 0
        self.armor = 0
        self.exp = 0
        self.keyboard = 0

    # Информация о мобе
    def info(self):
        string = f'''Здоровье: {self.health}
Атака: {self.damage}
Броня: {self.armor}'''
        return string

    # Метод для получения урона от игрока
    def attack(self, damage):
        self.health -= damage * (1 - calculate_armor(self.armor))

    # Метод для подсчета выдаваемого опыта за убийство
    def get_exp(self, player_level):
        percent = self.exp * 0.1
        exp = randint(self.exp - percent, self.exp + percent)
        x = player_level - self.level
        return round((2 * exp) / (1 + math.exp(x / 10)))


# Класс Гоблина
class Goblin(Enemy):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.health = 50
        self.damage = 3
        self.armor = 0
        self.exp = 50
        self.keyboard = ikb.goblin


# Класс Скелета
class Skeleton(Enemy):
    def __init__(self):
        super().__init__()
        self.level = 5
        self.health = 150
        self.damage = 10
        self.armor = 2
        self.exp = 90
        self.keyboard = ikb.skeleton


# Класс Энта
class Ent(Enemy):
    def __init__(self):
        super().__init__()
        self.level = 10
        self.health = 350
        self.damage = 15
        self.armor = 5
        self.exp = 170
        self.keyboard = ikb.skeleton
