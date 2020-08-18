import keyboards as kb
from calculating import *
import time
from threading import Timer
import levels
from config import DATABASE


# Класс игрока
class Player:
    def __init__(self, user_id):
        self.id = user_id

    @property
    def keyboard(self):
        name = DATABASE.get_attr_by_id(self.id, ('current_keyboard',))['current_keyboard']
        return kb.return_keyboard(name)

    @property
    def damage(self):
        main_stat = DATABASE.get_attr_by_id(self.id, ('main_stat',))['main_stat']
        stats = DATABASE.get_attr_by_id(self.id, (f'{main_stat}', 'agility'))
        damage = stats[f'{main_stat}'] + (1 + 0.02 * stats['agility'])
        return damage

    # Информация об игроке
    def __str__(self):
        stats = DATABASE.get_attr_by_id(self.id,
                                        ('user_name', 'class', 'user_level', 'current_exp', 'strength',
                                         'agility', 'intelligence',
                                         'health', 'max_health', 'health_per_second', 'armor'))

        string = f'''Имя: {stats['user_name']}
Класс: {stats['class']}
Уровень: {stats['user_level']}
Опыт: {stats['current_exp']} / {levels.levels[stats['user_level']]}
Сила: {round(stats['strength'], 2)}
Ловкость: {round(stats['agility'], 2)}
Интеллект: {round(stats['intelligence'], 2)}
Здоровье: {round(stats['health'], 2)} / {stats['max_health']}
Регенерация: {round(stats['health_per_second'], 2)} здоровья в секунду
Атака: {round(self.damage)}
Броня: {round(stats['armor'])}'''
        return string

    # Метод для смены имени
    def change_name(self, message, bot):
        DATABASE.update_by_id(self.id, 'user_name', f"'{message.text}'")
        bot.send_message(message.chat.id, 'Имя изменено')

    # Метод для смены клавиатуры
    def change_keyboard(self, name):
        DATABASE.update_by_id(self.id, 'current_keyboard', f"'{name}'")

    # Метод для перехода на новый уровень
    def next_level(self):
        stats = DATABASE.get_attr_by_id(self.id, ('user_level', 'agility', 'strength', 'intelligence', 'class'))
        level = stats['user_level']
        agility = stats['agility']
        strength = stats['strength']
        intelligence = stats['intelligence']
        user_class = stats['class']

        strength_const = []
        agility_const = []
        intelligence_const = []
        if user_class == 'Воин':
            strength_const = [2, 1.05]
            agility_const = [1.3, 1.03]
            intelligence_const = [1.1, 1.01]
        elif user_class == 'Лучник':
            strength_const = [1.1, 1.01]
            agility_const = [2, 1.05]
            intelligence_const = [1.3, 1.03]
        elif user_class == 'Маг':
            strength_const = [1.3, 1.03]
            agility_const = [1.1, 1.01]
            intelligence_const = [2, 1.05]

        add_strength = calculate_exponential_grow_with_round(strength_const[0], strength_const[1], level, 2)
        add_agility = calculate_exponential_grow_with_round(agility_const[0], agility_const[1], level, 2)
        add_intelligence = calculate_exponential_grow_with_round(intelligence_const[0], intelligence_const[1], level, 2)

        strength += add_strength
        agility += add_agility
        intelligence += add_intelligence

        DATABASE.update_by_id(self.id, 'strength', strength)
        DATABASE.update_by_id(self.id, 'agility', agility)
        DATABASE.update_by_id(self.id, 'intelligence', intelligence)

        level += 1
        DATABASE.update_by_id(self.id, 'user_level', level)
        return add_strength, add_agility, add_intelligence

    # Метод для востановления здоровья
    def heal(self):
        stats = DATABASE.get_attr_by_id(self.id, ('health', 'max_health', 'health_per_second'))
        health = stats['health']
        max_health = stats['max_health']
        health_per_second = stats['health_per_second']

        if health < max_health:
            health += health_per_second
            if health > max_health:
                health = max_health

        DATABASE.update_by_id(self.id, 'health', health)

    # Метод для возрождения
    def resurrect(self, bot):
        stats = DATABASE.get_attr_by_id(self.id, ('max_health',))
        max_health = stats['max_health']

        health = int(max_health * 0.1)
        is_death = False

        DATABASE.update_by_id(self.id, 'health', health)
        DATABASE.update_by_id(self.id, 'is_death', is_death)

        bot.send_message(self.id, 'Вы возродились')

    # Метод для создания таймера на возрождение
    def resurrect_timer(self, bot):
        stats = DATABASE.get_attr_by_id(self.id, ('time_for_resurrect',))
        time_for_resurrect = stats['time_for_resurrect']

        time_to_start_resurrect = time.time()
        timer = Timer(time_for_resurrect, self.resurrect, [bot])

        DATABASE.update_by_id(self.id, 'time_to_start_resurrect', time_to_start_resurrect)

        try:
            timer.start()

        except Exception as e:
            timer.cancel()
            self.resurrect(bot)
            print(e)

    # Метод для битвы с мобом
    def mob_attack(self, other, bot):
        stats = DATABASE.get_attr_by_id(self.id, ('health', 'armor', 'user_level', 'current_exp'))
        health = stats['health']
        armor = stats['armor']
        level = stats['user_level']
        current_exp = stats['current_exp']
        # Цикл битвы до смерти
        while other.health > 0 and health > 0:
            health -= int(other.damage * (1 - calculate_armor(armor)))
            other.attack(self.damage)

        else:
            # Проверка на смерть кого-либо
            if health <= 0:
                health = 0
                is_death = True

                DATABASE.update_by_id(self.id, 'health', health)
                DATABASE.update_by_id(self.id, 'is_death', is_death)

                self.resurrect_timer(bot)
                return 'death', 0, 0

            elif other.health <= 0:
                DATABASE.update_by_id(self.id, 'health', health)
                add_exp = other.get_exp(level)
                current_exp += add_exp
                DATABASE.update_by_id(self.id, 'current_exp', current_exp)
                next_level = levels.next_level(self)
                return 'kill', add_exp, next_level
