import config
from Player import Player


# Обработка комманды /start
@config.BOT.message_handler(commands=['start'])
def start_message(message):
    id = message.chat.id
    if not(message.chat.id in config.DATABASE.players):
        config.DATABASE.players[id] = Player(id, message.chat.username)
        config.DATABASE.safe_changes()
    config.BOT.send_message(id, 'Давай начнем',
                            reply_markup=config.DATABASE.players[id].keyboard)


# Обработка команды Игры
@config.BOT.message_handler(func=lambda message: True if (message.text.lower() == 'игры') else False,
                            content_types=['text'])
def games(message):
    config.DATABASE.players[message.chat.id].change_keyboard('games')
    config.BOT.send_message(message.chat.id, 'Игры',
                            reply_markup=config.DATABASE.players[message.chat.id].keyboard)


# Обработка комманды TelegramRPG
@config.BOT.message_handler(func=lambda message: True if message.text.lower() == 'telegramrpg' else False,
                            content_types=['text'])
def game_telegramrpg(message):
    welcome = f'''
Добро пожаловать в TelegramRPG
Это захватывающая текстовая RPG
'''
    config.DATABASE.players[message.chat.id].change_keyboard('telegramrpg')
    config.BOT.send_message(message.chat.id, welcome,
                            reply_markup=config.DATABASE.players[message.chat.id].keyboard)


# Обработка команды Назад
@config.BOT.message_handler(func=lambda message: True if (message.text.lower() == 'назад') else False,
                            content_types=['text'])
def back(message):
    id = message.chat.id
    player = config.DATABASE.players[id]
    if player.current_keyboard == 'games':
        keyboard = 'main'
    elif player.current_keyboard == 'telegramrpg':
        keyboard = 'games'
    else:
        return 0
    config.DATABASE.players[id].change_keyboard(keyboard)
    config.BOT.send_message(id, 'Назад',
                            reply_markup=config.DATABASE.players[id].keyboard)


# Обработка игры TelegramRPG
@config.BOT.message_handler(func=lambda message:
                            True if config.DATABASE.players[message.chat.id].current_keyboard == 'telegramrpg' else False,
                            content_types=['text'])
def telegramrpg(message):
    id = message.chat.id
    if message.text.lower() == 'персонаж':
        config.BOT.send_message(id, str(config.DATABASE.players[id]))
    else:
        error(message)


# Обработка остальных текстовых сообщений
@config.BOT.message_handler(content_types=['text'])
def error(message):
    print(config.DATABASE.players[message.chat.id].current_keyboard)
    config.BOT.send_message(message.chat.id, 'Я даже не знаю, что вам сказать...')
