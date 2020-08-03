from config import BOT, DATABASE
from player import Player
from enemy import Enemy, Goblin, Skeleton
import inline_keyboards as ikb
import time


# Обработка комманды /start
@BOT.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id

    if not(user_id in DATABASE.players):
        DATABASE.players[user_id] = Player(user_id, message.chat.username)
        DATABASE.safe_changes()
    BOT.send_message(user_id, 'Давай начнем',
                     reply_markup=DATABASE.players[user_id].keyboard)


# Обработка команды Игры
@BOT.message_handler(func=lambda message: True if message.text.lower() == 'игры' else False,
                     content_types=['text'])
def games(message):
    DATABASE.players[message.chat.id].change_keyboard('games')
    BOT.send_message(message.chat.id, 'Игры',
                     reply_markup=DATABASE.players[message.chat.id].keyboard)


# Обработка комманды TelegramRPG
@BOT.message_handler(func=lambda message: True if message.text.lower() == 'telegramrpg' else False,
                     content_types=['text'])
def game_telegramrpg(message):
    welcome = '''Добро пожаловать в TelegramRPG
Это захватывающая текстовая RPG'''

    DATABASE.players[message.chat.id].change_keyboard('TelegramRPG.main')
    BOT.send_message(message.chat.id, welcome,
                     reply_markup=DATABASE.players[message.chat.id].keyboard)


# Обработка игры TelegramRPG
@BOT.message_handler(func=lambda message:
                     True if 'TelegramRPG' in DATABASE.players[message.chat.id].current_keyboard else False,
                     content_types=['text'])
def telegramrpg(message):
    user_id = message.chat.id
    text = message.text

    if text.lower() == 'персонаж':
        BOT.send_message(user_id, str(DATABASE.players[user_id]), reply_markup=ikb.person)
    elif text.lower() == 'локации':
        DATABASE.players[user_id].change_keyboard('TelegramRPG.locations.locations')
        BOT.send_message(user_id, 'Выбери локацию', reply_markup=DATABASE.players[user_id].keyboard)
    elif text.lower() == 'лес смерти':
        DATABASE.players[user_id].change_keyboard('TelegramRPG.locations.forest_of_death')
        BOT.send_message(user_id, 'Добро пожаловать в Лес смерти', reply_markup=DATABASE.players[user_id].keyboard)
    elif text.lower() == 'гоблин':
        info = Goblin().info()
        BOT.send_message(user_id, info, reply_markup=ikb.goblin)
    elif text.lower() == 'скелет':
        info = Skeleton().info()
        BOT.send_message(user_id, info, reply_markup=ikb.skeleton)
    elif text.lower() == 'назад':
        back_telegramrpg(user_id, DATABASE.players[user_id].current_keyboard)
    else:
        error(message)


# Обработка команды Назад
@BOT.message_handler(func=lambda message: True if message.text.lower() == 'назад' else False,
                     content_types=['text'])
def back(message):
    user_id = message.chat.id
    player = DATABASE.players[user_id]

    if player.current_keyboard == 'games':
        keyboard = 'main'
    else:
        return 0

    player.change_keyboard(keyboard)
    BOT.send_message(user_id, 'Назад',
                     reply_markup=player.keyboard)


# Обработка остальных текстовых сообщений
@BOT.message_handler(content_types=['text'])
def error(message):
    print(message.text)
    print(DATABASE.players[message.chat.id].current_keyboard)
    BOT.send_message(message.chat.id, 'Я даже не знаю, что вам сказать...')


def back_telegramrpg(user_id, keyboard):
    if keyboard == 'TelegramRPG.main':
        keyboard = 'games'
    elif keyboard == 'TelegramRPG.locations.locations':
        keyboard = 'TelegramRPG.main'
    elif keyboard == 'TelegramRPG.locations.forest_of_death':
        keyboard = 'TelegramRPG.locations.locations'
    else:
        print('error')
        return 0

    DATABASE.players[user_id].change_keyboard(keyboard)
    BOT.send_message(user_id, 'Назад',
                     reply_markup=DATABASE.players[user_id].keyboard)


@BOT.callback_query_handler(func=lambda call: True)
def inline_keyboards_handler(call):
    BOT.answer_callback_query(callback_query_id=call.id)
    user_id = call.message.chat.id

    if call.data == 'change_name':
        BOT.send_message(user_id, 'Введите новое имя')
        BOT.register_next_step_handler(call.message, DATABASE.players[user_id].change_name, BOT)

    elif call.data.startswith('attack'):
        if not DATABASE.players[user_id].is_death:
            result = 'none'
            enemy = Enemy()

            if 'goblin' in call.data:
                enemy = Goblin()
                result = DATABASE.players[user_id].mob_attack(enemy)
            elif 'skeleton' in call.data:
                enemy = Skeleton()
                result = DATABASE.players[user_id].mob_attack(enemy)

            if result[0] == 'kill':
                text = f'Вы победили\n' \
                       f'Вы получили {result[1]} опыта\n' \
                       f'Ваше здоровье:' \
                       f' {round(DATABASE.players[user_id].health, 2)} / {DATABASE.players[user_id].max_health}'
                BOT.send_message(user_id, text, reply_markup=enemy.keyboard)

                if result[2]:
                    text = f'Вы получили новый уровень:\n' \
                           f'Ваш уровень: {DATABASE.players[user_id].level}\n' \
                           f'Здоровье: {DATABASE.players[user_id].max_health} + {result[2][0]}\n' \
                           f'Урон: {DATABASE.players[user_id].damage} + {result[2][1]}'
                    BOT.send_message(user_id, text)

            elif result[0] == 'death':
                need_time = int(DATABASE.players[user_id].time_for_resurrect -
                                (time.time() - DATABASE.players[user_id].time_to_start_resurrect))
                if need_time > 60:
                    minutes = need_time // 60
                    need_time -= minutes * 60
                    need_time = f'{minutes} : {need_time}'
                elif need_time < 10:
                    need_time = f'0 : 0{need_time}'
                else:
                    need_time = f'0 : {need_time}'

                text = f'Вы погибли\n' \
                       f'Возрождение через:' \
                       f' {need_time}'
                BOT.send_message(user_id, text)

            elif result == 'none':
                error(call.message)
        else:
            need_time = int(DATABASE.players[user_id].time_for_resurrect -
                            (time.time() - DATABASE.players[user_id].time_to_start_resurrect))
            if need_time > 60:
                minutes = need_time // 60
                need_time -= minutes * 60
                need_time = f'{minutes} : {need_time}'
            elif need_time < 10:
                need_time = f'0 : 0{need_time}'
            else:
                need_time = f'0 : {need_time}'

            text = f'Вы погибли\n' \
                   f'Возрождение через:' \
                   f' {need_time}'
            BOT.send_message(user_id, text)
