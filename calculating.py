# ---
def calculate_armor(armor):
    return armor / (50 + armor)


def calculate_exponential_grow(x, exp, number):
    return round(x * exp ** number)
