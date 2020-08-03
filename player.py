import keyboards as kb
from calculating import calculate_armor
import time
from threading import Timer
from random import randint
import levels


class Player:

    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.max_health = 200
        self.health = 200
        self.health_per_second = 1
        self.damage = 10
        self.armor = 0
        self.level = 1
        self.current_exp = 0
        self.exp_to_next_level = 1000
        self.keyboard = kb.return_keyboard('main')
        self.current_keyboard = 'main'
        self.time_to_start_resurrect = 0
        self.time_for_resurrect = 3
        self.is_death = False

    def __str__(self):
        self.string = f'''Имя: {self.name}
Уровень: {self.level}
Опыт: {self.current_exp} / {levels.levels[self.level]}
Здоровье: {round(self.health, 2)} / {self.max_health}
Регенерация: {round(self.health_per_second, 2)} здоровья в секунду
Атака: {self.damage}
Броня: {self.armor}'''
        return self.string

    def change_name(self, message, bot):
        self.name = message.text
        bot.send_message(message.chat.id, 'Имя изменено')

    def change_keyboard(self, name):
        self.keyboard = kb.return_keyboard(name)
        self.current_keyboard = name

    def next_level(self):
        return levels.add_stats(self)

    def heal(self):
        if self.health < self.max_health:
            self.health += self.health_per_second
            self.health = self.health
            if self.health > self.max_health:
                self.health = self.max_health

    def resurrect(self):
        self.health = int(self.max_health * 0.1)
        self.is_death = False

    def resurrect_timer(self):
        self.time_to_start_resurrect = time.time()
        self.time_for_resurrect = self.level * 3
        timer = Timer(self.time_for_resurrect, self.resurrect)
        timer.start()

    def mob_attack(self, other):
        while other.health > 0 and self.health > 0:
            self.health -= int(other.damage * (1 - calculate_armor(self.armor)))
            other.attack(self.damage)

        else:
            if self.health <= 0:
                self.health = 0
                self.is_death = True
                self.resurrect_timer()
                return 'death', 0, 0

            elif other.health <= 0:
                add_exp = other.get_exp(self.level)
                self.current_exp += add_exp
                next_level = levels.next_level(self)
                return 'kill', add_exp, next_level
