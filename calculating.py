# Функция вычисления снижения урона
def calculate_armor(armor):
    return armor / (50 + armor)


# Функция для вычисления экспоненциального роста без округления
def calculate_exponential_grow(x, exp, number):
    return x * exp ** number


# Функция для вычисления экспоненциального роста
def calculate_exponential_grow_with_round(x, exp, number, n=0):
    return round(x * exp ** number, n)
