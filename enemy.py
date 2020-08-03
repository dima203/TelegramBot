from calculating import calculate_armor


class Enemy:
    def __init__(self):
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


class Goblin(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.damage = 3
        self.armor = 0
        self.exp = 40
