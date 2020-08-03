import telebot


person = telebot.types.InlineKeyboardMarkup(True)
person.add(telebot.types.InlineKeyboardButton(text='Сменить имя', callback_data='change_name'))

goblin = telebot.types.InlineKeyboardMarkup(True)
goblin.add(telebot.types.InlineKeyboardButton(text='Атаковать', callback_data='attack_goblin'))

skeleton = telebot.types.InlineKeyboardMarkup(True)
skeleton.add(telebot.types.InlineKeyboardButton(text='Атаковать', callback_data='attack_skeleton'))
