import pickle
from Player import Player


# Класс базы данных
class DataBase:

    def __init__(self, name):
        self.name = name
        try:
            self.file = open(self.name, 'rb')
            self.players = pickle.load(self.file)
            self.file.close()
        except FileNotFoundError:
            self.file = open(self.name, 'wb')
            self.players = {
                0: Player('Admin', 'Admin')
            }
            pickle.dump(self.players, self.file)
            self.file.close()

    def safe_changes(self):
        self.file = open(self.name, 'wb')
        pickle.dump(self.players, self.file)
        self.file.close()

    def remake_database(self):
        self.players = {
            0: Player('Admin', 'Admin')
        }
        self.safe_changes()
