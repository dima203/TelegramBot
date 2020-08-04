import pickle
from player import Player


# Класс базы данных
class DataBase:

    def __init__(self, name):
        self.name = name

        try:
            # Загрузка игроков
            self.file = open(self.name, 'rb')
            self.players = pickle.load(self.file)
            self.file.close()

        except FileNotFoundError:
            # При отсутствии файла создаёт новый
            self.remake_database()

        except EOFError:
            # При отсутствии данных в файле пересоздаёи заново
            self.remake_database()

# Сохранение изменений БД
    def safe_changes(self):
        self.file = open(self.name, 'wb')
        pickle.dump(self.players, self.file)
        self.file.close()

# Пересоздание БД с 1 элементом Админа
# При желании можно вместо нуля поставить свой id
    def remake_database(self):
        self.players = {0: Player('Admin', 'Admin')}
        self.safe_changes()
