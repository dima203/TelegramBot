from telebot import TeleBot as Bot
from file import DataBase
import secret


# Создание бота по токену из BotFather
BOT = Bot(secret.token)

# Открытие "базы данных"
DATABASE = DataBase('1.data')

if __name__ == '__main__':
    DATABASE.remake_database()
