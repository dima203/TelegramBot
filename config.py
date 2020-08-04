from telebot import TeleBot as Bot
from file import DataBase
import secret
import subprocess


# Загрузка PyTelegramBotAPI
subprocess.run("pip3 install --upgrade PyTelegramBotAPI", shell=True)

# Создание бота по токену из BotFather
BOT = Bot(secret.token)  # <--- Свой токен подставлять сюда в ковычках. Пример: "Ваш токен"

# Открытие "базы данных"
DATABASE = DataBase('Players.data')

# Пересоздание базы данных
if __name__ == '__main__':
    DATABASE.remake_database()
