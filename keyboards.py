import telebot


# Основная клавиатура. Появляется после комманды /start
main = telebot.types.ReplyKeyboardMarkup(True)
main.row('Игры')

# Клавиатура с играми. Появляется после комманды Игры
games = telebot.types.ReplyKeyboardMarkup(True)
games.row('TelegramRPG')
games.row('Назад')


# ---
class Location:
    locations = telebot.types.ReplyKeyboardMarkup(True)
    locations.row('Лес смерти')
    locations.row('Назад')

    forest_of_death = telebot.types.ReplyKeyboardMarkup(True)
    forest_of_death.row('Гоблин', 'Скелет')
    forest_of_death.row('Назад')


# Клавиатура игры TelgramRPG. Появляется после комманы TelegramRPG
class TelegramRPG:
    main = telebot.types.ReplyKeyboardMarkup(True)
    main.row('Персонаж', 'Инвентарь', 'Квесты', 'Локации')
    main.row('Арена', 'Таблица лидеров', 'Достижения')
    main.row('Назад')

    locations = Location()


# Возврат клавиатуры по её имени
def return_keyboard(name):
    return eval(f'{name}')
