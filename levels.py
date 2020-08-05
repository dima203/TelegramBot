from calculating import calculate_exponential_grow_with_round


# Создание словаря типа уровень: опыт для перехода на следующий
levels = {
    1: 1000,
}

# Внесение значений
for i in range(99):
    levels[i + 1] = calculate_exponential_grow_with_round(1000, 1.1, i)


# Проверка перехода на следующий уровень
def next_level(player):
    if player.level >= 100:
        return False
    if player.current_exp >= levels[player.level]:
        player.current_exp -= levels[player.level]
        stats = player.next_level()
        return stats
    else:
        return False
