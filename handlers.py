from config import BOT, DATABASE
from player import Player
from enemy import Goblin, Skeleton, Ent
import levels
import keyboards
import inline_keyboards as ikb
import time


# Обработка команды /start
@BOT.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    BOT.send_message(user_id, 'Давай начнем', reply_markup=keyboards.main)


# Обработка команды Игры
@BOT.message_handler(func=lambda message: True if message.text.lower() == 'игры' else False,
                     content_types=['text'])
def games(message):
    BOT.send_message(message.chat.id, 'Игры', reply_markup=keyboards.games)


# Обработка команды TelegramRPG
@BOT.message_handler(func=lambda message: True if message.text.lower() == 'telegramrpg' else False,
                     content_types=['text'])
def game_telegramrpg(message):
    welcome = '''Добро пожаловать в TelegramRPG
Это захватывающая текстовая RPG'''
    user_id = message.chat.id

    if not (DATABASE.chek_id_in_db(user_id)):
        BOT.send_message(user_id, welcome, reply_markup=keyboards.change_class)
        BOT.register_next_step_handler(message, change_class)
    else:
        Player(user_id).change_keyboard('TelegramRPG.main')
        BOT.send_message(user_id, welcome, reply_markup=Player(user_id).keyboard)


# Проверка наличия игрока в БД
@BOT.message_handler(func=lambda message: False if DATABASE.chek_id_in_db(message.chat.id) else True,
                     content_types=['text'])
def warning(message):
    BOT.send_message(message.chat.id, 'Напишите команду /start', reply_markup=keyboards.start)


# Обработка игры TelegramRPG
@BOT.message_handler(func=lambda message:
                     True if 'TelegramRPG' in DATABASE.get_attr_by_id(message.chat.id,
                                                                      ('current_keyboard',))['current_keyboard']
                     else False,
                     content_types=['text'])
def telegramrpg(message):
    user_id = message.chat.id
    text = message.text

    if text.lower() == 'персонаж':
        BOT.send_message(user_id, str(Player(user_id)), reply_markup=ikb.person)
    elif text.lower() == 'локации':
        Player(user_id).change_keyboard('TelegramRPG.locations.locations')
        BOT.send_message(user_id, 'Выбери локацию', reply_markup=Player(user_id).keyboard)
    elif text.lower() == 'лес смерти':
        Player(user_id).change_keyboard('TelegramRPG.locations.forest_of_death')
        BOT.send_message(user_id, 'Добро пожаловать в Лес смерти', reply_markup=Player(user_id).keyboard)
    elif text.lower() == 'гоблин':
        info = Goblin().info()
        BOT.send_message(user_id, info, reply_markup=ikb.goblin)
    elif text.lower() == 'скелет':
        info = Skeleton().info()
        BOT.send_message(user_id, info, reply_markup=ikb.skeleton)
    elif text.lower() == 'энт':
        info = Ent().info()
        BOT.send_message(user_id, info, reply_markup=ikb.ent)
    elif text.lower() == 'назад':
        back_telegramrpg(user_id, DATABASE.get_attr_by_id(user_id, ('current_keyboard',))['current_keyboard'])
    else:
        in_process(user_id)


# Обработка команды Назад
@BOT.message_handler(func=lambda message: True if message.text.lower() == 'назад' else False,
                     content_types=['text'])
def back(message):
    user_id = message.chat.id
    current_keyboard = DATABASE.get_attr_by_id(user_id, ('current_keyboard',))['current_keyboard']

    if current_keyboard == 'games':
        keyboard = 'main'
    else:
        return 0

    Player(user_id).change_keyboard(keyboard)
    BOT.send_message(user_id, 'Назад',
                     reply_markup=Player(user_id).keyboard)


# Обработка остальных текстовых сообщений
@BOT.message_handler(content_types=['text'])
def error(message):
    print(message.text)  # Отладочные сообщения
    print(DATABASE.get_attr_by_id(message.chat.id, ('current_keyboard',))['current_keyboard'])  # Отладочные сообщения
    BOT.send_message(message.chat.id, 'Я даже не знаю, что вам сказать...')


# Обработка команды назад для игры TelegramRPG
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

    Player(user_id).change_keyboard(keyboard)
    BOT.send_message(user_id, 'Назад',
                     reply_markup=Player(user_id).keyboard)


def in_process(user_id):
    BOT.send_message(user_id, 'В разработке')


# Функция выбора класса
def change_class(message):
    user_id = message.chat.id

    while True:
        if message.text == 'Воин':
            DATABASE.add_user(user_id, message.chat.username, 'warrior')
        elif message.text == 'Лучник':
            DATABASE.add_user(user_id, message.chat.username, 'archer')
        elif message.text == 'Маг':
            DATABASE.add_user(user_id, message.chat.username, 'mage')
        else:
            BOT.send_message(user_id, 'Неверный класс')
            BOT.register_next_step_handler(message, change_class)
            return 0
        break

    Player(user_id).change_keyboard('TelegramRPG.main')
    BOT.send_message(user_id, 'Персонаж создан\nВперед, к приключениям',
                     reply_markup=Player(user_id).keyboard)


#
def confirm(message, func, keyboard, text):
    user_id = message.chat.id
    if message.text == 'Подтвердить':
        BOT.send_message(user_id, text, reply_markup=keyboard)
        BOT.register_next_step_handler(message, func)
    elif message.text == 'Отмена':
        BOT.send_message(user_id, 'Отмена', reply_markup=Player(user_id).keyboard)
    else:
        BOT.send_message(user_id, 'Неверный ввод', reply_markup=Player(user_id).keyboard)


# Обработка инлайн клавиатур
@BOT.callback_query_handler(func=lambda call: True if DATABASE.chek_id_in_db(call.message.chat.id)
                            else warning(call.message))
def inline_keyboards_handler(call):
    BOT.answer_callback_query(callback_query_id=call.id)
    user_id = call.message.chat.id

    # Обработка смены имени
    if call.data == 'change_name':
        BOT.send_message(user_id, 'Введите новое имя')
        BOT.register_next_step_handler(call.message, Player(user_id).change_name, BOT)

    # Обработка атаки моба
    elif call.data.startswith('attack'):
        if not DATABASE.get_attr_by_id(user_id, ('is_death',))['is_death']:
            enemy = 'none'

            # Выбор моба
            if 'goblin' in call.data:
                enemy = Goblin()
            elif 'skeleton' in call.data:
                enemy = Skeleton()
            elif 'ent' in call.data:
                enemy = Ent()

            # Проверка на ниличие моба
            if enemy == 'none':
                result = 'none'
            else:
                result = Player(user_id).mob_attack(enemy, BOT)

            if result == 'none':
                error(call.message)

            # Победа
            elif result[0] == 'kill':
                text = f'Вы победили\n' \
                       f'Вы получили {result[1]} опыта\n' \
                       f'Ваше здоровье:' \
                       f" {round(DATABASE.get_attr_by_id(user_id, ('health',))['health'], 2)} / " \
                       f"{DATABASE.get_attr_by_id(user_id, ('max_health',))['max_health']}"
                BOT.send_message(user_id, text, reply_markup=enemy.keyboard)

                # Проверка перехода на новый уровень
                if result[2]:
                    next_level = result[2]
                    while next_level:
                        text = f'Вы получили новый уровень:\n' \
                               f'Ваш уровень: {DATABASE.get_attr_by_id(user_id, ("user_level",))["user_level"]}\n' \
                               f'Сила: {round(DATABASE.get_attr_by_id(user_id, ("strength",))["strength"], 2)}' \
                               f' + {next_level[0]}\n' \
                               f'Ловкость: {round(DATABASE.get_attr_by_id(user_id, ("agility",))["agility"], 2)}' \
                               f' + {next_level[1]}\n' \
                               f'Интеллект:' \
                               f' {round(DATABASE.get_attr_by_id(user_id, ("intelligence",))["intelligence"], 2)}' \
                               f' + {next_level[2]}'
                        BOT.send_message(user_id, text)
                        next_level = levels.next_level(Player(user_id))

            # Смерть
            elif result[0] == 'death':
                need_time = int(DATABASE.get_attr_by_id(user_id, ('time_for_resurrect',))['time_for_resurrect'] -
                                (time.time() - DATABASE.get_attr_by_id(user_id,
                                                                       ('time_to_start_resurrect',))
                                ['time_to_start_resurrect']))
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

        else:
            # Обработка, если персонаж уже мертв
            need_time = int(DATABASE.get_attr_by_id(user_id, ('time_for_resurrect',))['time_for_resurrect'] -
                            (time.time() - DATABASE.get_attr_by_id(user_id,
                                                                   ('time_to_start_resurrect',))
                            ['time_to_start_resurrect']))
            if need_time > 60:
                minutes = need_time // 60
                need_time -= minutes * 60
                need_time = f'{minutes} : {need_time}'
            elif need_time < 0:
                Player(user_id).resurrect(BOT)
                return 0
            elif need_time < 10:
                need_time = f'0 : 0{need_time}'
            else:
                need_time = f'0 : {need_time}'

            text = f'Вы погибли\n' \
                   f'Возрождение через:' \
                   f' {need_time}'
            BOT.send_message(user_id, text)

    elif call.data == 'change_class':
        BOT.send_message(user_id, 'При смене класса вы потеряете весь прогресс\nВы уверены?',
                         reply_markup=keyboards.confirm)
        BOT.register_next_step_handler(call.message, confirm, change_class, keyboards.change_class, 'Выбери класс')
