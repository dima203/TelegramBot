import telebot


main = telebot.types.ReplyKeyboardMarkup(True)
main.row('Игры')

games = telebot.types.ReplyKeyboardMarkup(True)
games.row('TelegramRPG')
games.row('Назад')

telegramrpg = telebot.types.ReplyKeyboardMarkup(True)
telegramrpg.row('Персонаж', 'Инвентарь', 'Квесты', 'Локации')
telegramrpg.row('Арена', 'Таблица лидеров')
telegramrpg.row('Назад')


def return_keyboard(name):
    return eval(f'{name}')