from calculating import calculate_exponential_grow, calculate_exponential_grow_with_round


levels = {
    1: 1000,
}

for i in range(99):
    levels[i + 1] = calculate_exponential_grow_with_round(1000, 1.2, i)


def next_level(player):
    if player.current_exp >= levels[player.level]:
        player.current_exp -= levels[player.level]
        stats = player.next_level()
        return stats
    else:
        return False


def add_stats(player):
    add_health = calculate_exponential_grow_with_round(50, 1.03, player.level)
    add_damage = calculate_exponential_grow_with_round(3, 1.03, player.level)
    add_health_per_second = calculate_exponential_grow(0.5, 1.01, player.level)

    player.max_health += add_health
    player.health_per_second += add_health_per_second
    player.health += add_health
    player.damage += add_damage
    player.level += 1

    return add_health, add_damage
