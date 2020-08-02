import telebot
import keyboards as kb


class Player:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.health = 200
        self.damage = 10
        self.level = 1
        self.keyboard = kb.return_keyboard('main')
        self.current_keyboard = 'main'

    def __str__(self):
        self.string = f'''
Имя: {self.name}
lvl: {self.level}
hp: {self.health}
damage: {self.damage}
'''
        return self.string

    def mob_attack(self):
        pass

    def change_keyboard(self, name):
        self.keyboard = kb.return_keyboard(name)
        self.current_keyboard = name
