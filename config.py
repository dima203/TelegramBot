from telebot import TeleBot as Bot
from file import DataBase
import secret


# Создание бота по токену из BotFather
BOT = Bot(secret.token) #<--- Свой токен подставлять сюда в ковычках. Пример: "Ваш токен" 

# Открытие "базы данных"
DATABASE = DataBase('Players.data')

# Пересоздание базы данных
if __name__ == '__main__':
    DATABASE.remake_database()
