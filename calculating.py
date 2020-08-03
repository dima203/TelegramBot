# ---
def calculate_armor(armor):
    return armor / (50 + armor)


def calculate_exponential_grow(x, exp, number):
    return x * exp ** number


def calculate_exponential_grow_with_round(x, exp, number):
    return round(x * exp ** number)
