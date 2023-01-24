# Файловая база данных SQL, которая поставляется в комплекте с Python и
# может использоваться в приложениях Python, устраняя необходимость
# устанавливать дополнительное программное обеспечение
import sqlite3
import difflib
import random
import pandas
import openpyxl

# Класс, в котором описаны методы взаимодействия с базой данных "LeoMarchBot"
import pandas as pd

class DataBaseWork:
    connector = ''

    # Создание базы данных "LeoMarchBot" (если еще не была создана)
    # и установка связи с ней
    def create_db(self):
        self.connector = sqlite3.connect('KTinder.db')

    # Создание таблицы "users"
    def create_table_users(self):
        with self.connector:
            self.connector.execute("""
                    CREATE TABLE IF NOT EXISTS users ( 
                        user_id INTEGER NOT NULL PRIMARY KEY,
                        user_nickname TEXT NOT NULL,
                        user_name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        gender TEXT NOT NULL,
                        opposite TEXT NOT NULL,
                        city TEXT NOT NULL,
                        dop_info TEXT NOT NULL,
                        description TEXT NOT NULL,
                        photo_or_video_id TEXT NOT NULL,
                        changes INTEGER NOT NULL,
                        current_state TEXT NOT NULL
                    );
                """)

    def create_admins_table(self):
        with self.connector:
            self.connector.execute("""
                    CREATE TABLE IF NOT EXISTS admins (
                        user_id INTEGER NOT NULL PRIMARY KEY,
                        mailing_to TEXT
                    );
                """)

    # def create_violators_table(self):
    #     with self.connector:
    #         self.connector.execute("""
    #                 CREATE TABLE IF NOT EXISTS violators (
    #                     user_id INTEGER NOT NULL PRIMARY KEY,
    #                     status TEXT
    #                 );
    #             """)

    # Добавление пользователя в таблицу "users"
    def add_user_in_users_table(self, user_id, user_nickname):
        with self.connector:
            self.connector.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                                   [user_id, user_nickname, '', 0, '', '', '', '', '', '', 0, ''])

    def add_user_in_admins_table(self, user_id):
        with self.connector:
            self.connector.execute(f"INSERT INTO admins VALUES(?, ?);",
                                   [user_id, ''])

    # Добавление данных пользователя в таблицу "users"
    def set_data_in_table(self, colomn_name, value, user_id, table_name):
        with self.connector:
            update = self.connector.execute(
                f"UPDATE {table_name} SET {colomn_name} = ? WHERE user_id = ?", (value, user_id,))

    # Проверка на существование пользователя в таблице с названием,
    # которое ранится в переменной "table_name"
    def is_exist_user_in_db(self, user_id, table_name):
        try:
            with self.connector:
                current_id = self.connector.execute(f"SELECT user_id FROM {table_name} WHERE user_id = {user_id}").fetchone()[0]
                return True
        except:
            return False

    # Получение данных пользователя из таблицы "users"
    def get_data_from_profiles_table(self, colomn_name, user_id):
        data = self.connector.execute(f"SELECT {colomn_name} FROM users WHERE user_id = '{user_id}'")
        return data.fetchone()[0]

    def get_data_from_admins_table(self, colomn_name, user_id):
        data = self.connector.execute(f"SELECT {colomn_name} FROM admins WHERE user_id = '{user_id}'")
        return data.fetchone()[0]

    # Получение id другого пользователя по схожим параметрам: "город" и "кто нравится"
    def find_other_profiles(self, self_id, self_city, self_gender):
        other_gender = ''
        if self_gender == 'Я парень':
            other_gender = 'Я девушка'
        elif self_gender == 'Я девушка':
            other_gender = 'Я парень'
        elif self_gender == 'Все равно':
            other_gender = None

        with self.connector:
            if other_gender == 'Я девушка' or other_gender == 'Я парень':
                others_id = self.connector.execute("SELECT user_id FROM users WHERE city = ? and gender = ?",
                                                   [self_city, other_gender, ]).fetchall()
            else:
                others_id = self.connector.execute("SELECT user_id FROM users WHERE city = ?",
                                                   [self_city, ]).fetchall()

            while True:
                current_other_id = int(others_id[random.randint(0, len(others_id) - 1)][0])

                if current_other_id != self_id:
                    return current_other_id

    # Получение id всех пользователей
    def get_all_users_id(self):
        all_id = self.connector.execute("SELECT * FROM users").fetchall()

        list_all_id = []

        for i in range(len(all_id)):
            list_all_id.append(int(all_id[i][0]))

        return list_all_id

    # Получение id всех пользователей, исходя из заданного ограничения по полу
    def get_all_specific_users_id(self, gender):
        if gender == 'Девушкам':
            gender = 'Я девушка'
        elif gender == 'Парням':
            gender = 'Я парень'

        list_all_specific_users_id = []

        all_specific_users_id = self.connector.execute(
            f"SELECT user_id FROM users WHERE gender = '{gender}'").fetchall()

        for i in range(len(all_specific_users_id)):
            list_all_specific_users_id.append(int(all_specific_users_id[i][0]))

        return list_all_specific_users_id

    def read_sql_to_frame(self):
        con = sqlite3.connect('KTinder.db')
        df = pd.read_sql_query("SELECT * FROM users", con)
        df.to_excel('Статистика.xlsx')

db = DataBaseWork()

# if __name__ == '__main__':
#     db = DataBaseWork()
#     db.create_db()
#     db.create_table_users()
#     print(db.get_all_specific_users_id('Девушкам'))