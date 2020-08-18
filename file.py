import pyodbc


# Класс базы данных
class DataBase:

    def __init__(self, path: str):
        self.path = path

        # Загрузка БД
        self.connection = pyodbc.connect(rf'Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};'
                                         rf'DBQ={path}')
        self.cursor = self.connection.cursor()

    def add_user(self, user_id, user_name, user_class):
        if user_id in self.get_ids():
            self.delete_by_id(user_id)
        if user_class == 'warrior':
            self.add_warrior(user_id, user_name)
        elif user_class == 'archer':
            self.add_archer(user_id, user_name)
        elif user_class == 'mage':
            self.add_mage(user_id, user_name)

    def add_warrior(self, user_id, user_name):
        self.add_new_record(user_id,
                            ('user_name', 'class', 'main_stat', 'agility', 'strength', 'intelligence'),
                            (f"'{user_name}'", "'Воин'", "'strength'", 6, 10, 2))
        self.update_by_id(user_id, 'health', self.get_attr_by_id(user_id, ('max_health',))['max_health'])

    def add_archer(self, user_id, user_name):
        self.add_new_record(user_id,
                            ('user_name', 'class', 'main_stat', 'agility', 'strength', 'intelligence'),
                            (f"'{user_name}'", "'Лучник'", "'agility'", 10, 2, 6))
        self.update_by_id(user_id, 'health', self.get_attr_by_id(user_id, ('max_health',))['max_health'])

    def add_mage(self, user_id, user_name):
        self.add_new_record(user_id,
                            ('user_name', 'class', 'main_stat', 'agility', 'strength', 'intelligence'),
                            (f"'{user_name}'", "'Маг'", "'intelligence'", 2, 6, 10))
        self.update_by_id(user_id, 'health', self.get_attr_by_id(user_id, ('max_health',))['max_health'])

    def clearing(self):
        self.cursor.execute('DELETE FROM users')
        self.connection.commit()

    def get_ids(self):
        res = []
        for i in self.cursor.execute('SELECT user_id from users'):
            res += i
        return res

    def get_attr_by_id(self, user_id, items):
        command = 'SELECT'

        for i in range(len(items)):
            if i == len(items) - 1:
                command += f' {items[i]}'
            else:
                command += f' {items[i]},'

        command += f' from users WHERE user_id = {user_id}'

        result = {}
        num = 0
        for row in self.cursor.execute(command):
            for i in row:
                result[items[num]] = i
                num += 1
        return result

    def update_by_id(self, user_id, item, new_value):
        command = f'UPDATE users SET {item} = {new_value} WHERE user_id = {user_id}'

        self.cursor.execute(command)
        self.connection.commit()

    def delete_by_id(self, user_id):
        command = f'DELETE FROM users WHERE user_id = {user_id}'

        self.cursor.execute(command)
        self.connection.commit()

    def add_new_record(self, user_id, items, values):
        command = f'INSERT INTO users ('
        command += f'user_id, '

        for i in range(len(items)):
            if i == len(items) - 1:
                command += f'{items[i]}) VALUES ('
            else:
                command += f'{items[i]}, '

        command += f'{user_id}, '
        for i in range(len(values)):
            if i == len(values) - 1:
                command += f'{values[i]})'
            else:
                command += f'{values[i]}, '

        self.cursor.execute(command)
        self.connection.commit()

    def chek_id_in_db(self, user_id):
        result = []

        for i in self.cursor.execute('SELECT user_id FROM users'):
            result += i

        if user_id in result:
            return True
        else:
            return False
