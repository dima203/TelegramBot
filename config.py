from telebot import TeleBot as Bot
from file import DataBase
import secret
import subprocess


# Загрузка PyTelegramBotAPI
subprocess.run('python.exe -m pip install --upgrade pip', shell=True)
subprocess.run('pip3 install --upgrade PyTelegramBotAPI', shell=True)

# Создание бота по токену из BotFather
BOT = Bot(secret.token)  # <--- Свой токен подставлять сюда в ковычках. Пример: "Ваш токен"

# Открытие "базы данных"
DATABASE = DataBase('C:/Users/Asus/PycharmProjects/Test_Bot/Players.accdb')

# Пересоздание базы данных
if __name__ == '__main__':
    DATABASE.clearing()
