import telebot


person = telebot.types.InlineKeyboardMarkup(True)
person.add(telebot.types.InlineKeyboardButton(text='Сменить имя', callback_data='change_name'))
