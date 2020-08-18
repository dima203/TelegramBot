from calculating import calculate_exponential_grow_with_round
from config import DATABASE


# Создание словаря типа уровень: опыт для перехода на следующий
levels = {
    1: 1000,
}

# Внесение значений
for i in range(99):
    levels[i + 1] = calculate_exponential_grow_with_round(1000, 1.1, i)


# Проверка перехода на следующий уровень
def next_level(player):
    user_stats = DATABASE.get_attr_by_id(player.id, ('user_level', 'current_exp'))
    level = user_stats['user_level']
    current_exp = user_stats['current_exp']
    if level >= 100:
        return False
    if current_exp >= levels[level]:
        current_exp -= levels[level]
        DATABASE.update_by_id(player.id, 'current_exp', current_exp)
        stats = player.next_level()
        return stats
    else:
        return False
