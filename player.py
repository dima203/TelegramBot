import keyboards as kb
from calculating import *
import time
from threading import Timer
import levels


# Класс игрока
class Player:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.player_class = 'none'
        self.main_stat = 'none'
        self.strength = 10
        self.agility = 10
        self.intelligence = 10
        self.health = self.max_health
        self.level = 1
        self.current_exp = 0
        self.keyboard = kb.return_keyboard('TelegramRPG.main')
        self.current_keyboard = 'TelegramRPG.main'
        self.time_to_start_resurrect = 0
        self.time_for_resurrect = 3
        self.is_death = False

    @property
    def max_health(self):
        return round(self.strength * 25)

    @property
    def health_per_second(self):
        return round(self.strength * 0.1, 2)

    @property
    def damage(self):
        if self.main_stat == 'none':
            return 0
        else:
            return round(eval(f'self.{self.main_stat}'))

    @property
    def armor(self):
        return round(self.agility / 3)

    # Информация об игроке
    def __str__(self):
        self.string = f'''Имя: {self.name}
Класс: {self.player_class}
Уровень: {self.level}
Опыт: {self.current_exp} / {levels.levels[self.level]}
Сила: {self.strength}
Ловкость: {self.agility}
Интеллект: {self.intelligence}
Здоровье: {round(self.health, 2)} / {self.max_health}
Регенерация: {round(self.health_per_second, 2)} здоровья в секунду
Атака: {self.damage}
Броня: {self.armor}'''
        return self.string

    # Метод для смены имени
    def change_name(self, message, bot):
        self.name = message.text
        bot.send_message(message.chat.id, 'Имя изменено')

    # Метод для смены клавиатуры
    def change_keyboard(self, name):
        self.keyboard = kb.return_keyboard(name)
        self.current_keyboard = name

    # Метод для перехода на новый уровень
    def next_level(self):
        add_strength = calculate_exponential_grow_with_round(2, 1.05, self.level)
        add_agility = calculate_exponential_grow_with_round(2, 1.05, self.level)
        add_intelligence = calculate_exponential_grow_with_round(2, 1.05, self.level)

        self.strength += add_strength
        self.agility += add_agility
        self.intelligence += add_intelligence

        self.level += 1
        return add_strength, add_agility, add_intelligence

    # Метод для востановления здоровья
    def heal(self):
        if self.health < self.max_health:
            self.health += self.health_per_second
            self.health = self.health
            if self.health > self.max_health:
                self.health = self.max_health

    # Метод для возрождения
    def resurrect(self, bot):
        self.health = int(self.max_health * 0.1)
        self.is_death = False
        bot.send_message(self.id, 'Вы возродились')

    # Метод для создания таймера на возрождение
    def resurrect_timer(self, bot):
        self.time_to_start_resurrect = time.time()
        self.time_for_resurrect = self.level * 3
        timer = Timer(self.time_for_resurrect, self.resurrect, [bot])

        try:
            timer.start()

        except Exception as e:
            timer.cancel()
            self.resurrect(bot)
            print(e)

    # Метод для битвы с мобом
    def mob_attack(self, other, bot):
        # Цикл битвы до смерти
        while other.health > 0 and self.health > 0:
            self.health -= int(other.damage * (1 - calculate_armor(self.armor)))
            other.attack(self.damage)

        else:
            # Проверка на смерть кого-либо
            if self.health <= 0:
                self.health = 0
                self.is_death = True
                self.resurrect_timer(bot)
                return 'death', 0, 0

            elif other.health <= 0:
                add_exp = other.get_exp(self.level)
                self.current_exp += add_exp
                next_level = levels.next_level(self)
                return 'kill', add_exp, next_level


# Класс Воина
class Warrior(Player):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.player_class = 'Воин'
        self.main_stat = 'strength'
        self.strength = 10
        self.agility = 6
        self.intelligence = 2
        self.health = self.max_health

    def next_level(self):
        add_strength = calculate_exponential_grow_with_round(2, 1.05, self.level)
        add_agility = calculate_exponential_grow_with_round(2, 1.03, self.level)
        add_intelligence = calculate_exponential_grow_with_round(2, 1.01, self.level)

        self.strength += add_strength
        self.agility += add_agility
        self.intelligence += add_intelligence

        self.level += 1
        return add_strength, add_agility, add_intelligence


# Класс Лучника
class Archer(Player):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.player_class = 'Лучник'
        self.main_stat = 'agility'
        self.strength = 2
        self.agility = 10
        self.intelligence = 6
        self.health = self.max_health

    def next_level(self):
        add_strength = calculate_exponential_grow_with_round(2, 1.01, self.level)
        add_agility = calculate_exponential_grow_with_round(2, 1.05, self.level)
        add_intelligence = calculate_exponential_grow_with_round(2, 1.03, self.level)

        self.strength += add_strength
        self.agility += add_agility
        self.intelligence += add_intelligence

        self.level += 1
        return add_strength, add_agility, add_intelligence


# Класс Мага
class Mage(Player):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.player_class = 'Маг'
        self.main_stat = 'intelligence'
        self.strength = 6
        self.agility = 3
        self.intelligence = 10
        self.health = self.max_health

    def next_level(self):
        add_strength = calculate_exponential_grow_with_round(2, 1.03, self.level)
        add_agility = calculate_exponential_grow_with_round(2, 1.01, self.level)
        add_intelligence = calculate_exponential_grow_with_round(2, 1.05, self.level)

        self.strength += add_strength
        self.agility += add_agility
        self.intelligence += add_intelligence

        self.level += 1
        return add_strength, add_agility, add_intelligence
