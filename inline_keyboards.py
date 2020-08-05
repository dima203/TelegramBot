import telebot


# Клавиатура для смены имени
person = telebot.types.InlineKeyboardMarkup(True)
person.add(telebot.types.InlineKeyboardButton(text='Сменить имя', callback_data='change_name'))
person.add(telebot.types.InlineKeyboardButton(text='Сменить класс', callback_data='change_class'))

# Клавиатура атки гоблино
goblin = telebot.types.InlineKeyboardMarkup(True)
goblin.add(telebot.types.InlineKeyboardButton(text='Атаковать', callback_data='attack_goblin'))

# Клавиатура атки скелета
skeleton = telebot.types.InlineKeyboardMarkup(True)
skeleton.add(telebot.types.InlineKeyboardButton(text='Атаковать', callback_data='attack_skeleton'))

# Клавиатура атки энта
ent = telebot.types.InlineKeyboardMarkup(True)
ent.add(telebot.types.InlineKeyboardButton(text='Атаковать', callback_data='attack_ent'))
