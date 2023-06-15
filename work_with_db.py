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
    # Создание базы данных "LeoMarchBot" (если еще не была создана)
    # и установка связи с ней
    def create_db(self):
        con = sqlite3.connect('KTinder.db')
        con.text_factory = lambda b: b.decode(errors='ignore')

        return con

    # Создание таблицы "users"
    def create_table_users(self):
        con = self.create_db()

        con.execute("""
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
                    is_matched BOOLEAN,
                    viewed_ids TEXT,
                    now_check_id INTEGER,
                    match_id TEXT,
                    last_action_time TEXT,
                    inactive INTEGER, 
                    mutual_id TEXT
                );
            """)

        #1# 71483094
        #2# 81646145
        #3# 71232662
        #4# 137713782

        con.commit()

    # Создание таблицы "admins"
    def create_admins_table(self):
        con = self.create_db()

        con.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    user_id INTEGER NOT NULL PRIMARY KEY,
                    violators_id INTEGER,
                    mailing_to TEXT,
                    photo_video_ids TEXT,
                    mail_text TEXT,
                    viewed_ids TEXT
                );
            """)

        con.commit()
################################
    def find_violator(self, self_id, status):
        con = self.create_db()

        viewed_ids = con.execute(
            f"SELECT viewed_ids FROM admins WHERE user_id = '{self_id}'").fetchone()[0]

        all_violators_id = con.execute(
            f"SELECT user_id FROM violators WHERE status = '{status}' AND number_of_complaints > 0").fetchall()

        con.commit()

        if len(viewed_ids.split()) == 1:
            if viewed_ids == '-1':
                for el in all_violators_id:
                    if str(el[0]) not in viewed_ids.split():
                        if DataBaseWork().is_exist_user_in_db(el[0], 'users') == False:
                            DataBaseWork().delete_user_from_violators_table(el[0])
                            continue

                        DataBaseWork().set_data_in_table('violators_id', all_violators_id[0][0], self_id, 'admins')
                        DataBaseWork().set_data_in_table('viewed_ids', all_violators_id[0][0], self_id, 'admins')
                        return all_violators_id[0][0]
            else:
                for el in all_violators_id:
                    if str(el[0]) not in viewed_ids.split():
                        if DataBaseWork().is_exist_user_in_db(el[0], 'users') == False:
                            DataBaseWork().delete_user_from_violators_table(el[0])
                            continue

                        DataBaseWork().set_data_in_table('violators_id', el[0], self_id, 'admins')
                        DataBaseWork().set_data_in_table('viewed_ids', viewed_ids + ' ' + str(el[0]), self_id, 'admins')
                        return el[0]
        else:
            for el in all_violators_id:
                if str(el[0]) not in viewed_ids.split():
                    if DataBaseWork().is_exist_user_in_db(el[0], 'users') == False:
                        DataBaseWork().delete_user_from_violators_table(el[0])
                        continue

                    DataBaseWork().set_data_in_table('violators_id', el[0], self_id, 'admins')
                    DataBaseWork().set_data_in_table('viewed_ids', viewed_ids + ' ' + str(el[0]), self_id, 'admins')
                    return el[0]

################################

    # Создание таблицы "violators"
    def create_violators_table(self):
        con = self.create_db()

        con.execute("""
                CREATE TABLE IF NOT EXISTS violators (
                    user_id INTEGER NOT NULL PRIMARY KEY,
                    status TEXT,
                    number_of_complaints INTEGER
                );
            """)

        con.commit()

    # Добавление пользователя в таблицу "users"
    def add_user_in_users_table(self, user_id, user_nickname):
        con = self.create_db()

        add = con.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
                               [user_id, user_nickname, '', -1, '', '', '', '', '', '', -1, 0, 'None', -1, '-1', '', 0, '-1'])

        con.commit()

    # Добавление пользователя в таблицу "admins"
    def add_user_in_admins_table(self, user_id):
        con = self.create_db()

        con.execute(f"INSERT INTO admins VALUES(?, ?, ?, ?, ?);",
                               [user_id, None, None, None, None, '-1'])
        con.commit()

    # Добавление пользователя в таблицу "violators"
    def add_user_in_violators_table(self, user_id):
        con = self.create_db()

        try:
            add_user = con.execute(f"INSERT INTO violators VALUES(?, ?, ?, ?);",
                                   [user_id, 'void', False, 1])
        except:
            value = con.execute(f"SELECT number_of_complaints FROM violators WHERE user_id = {user_id}").fetchone()[0]

            update = con.execute(
                f"UPDATE violators SET number_of_complaints = ? WHERE user_id = ?", (int(value)+1, user_id,))

        con.commit()

    # Удаление пользователя из таблицы "violators"
    def delete_user_from_violators_table(self, user_id):
        con = self.create_db()

        con.execute(f"DELETE FROM violators WHERE user_id = '{user_id}'")

        con.commit()

    # Удаление пользователя из таблицы "users"
    def delete_user_from_users_table(self, user_id):
        con = self.create_db()

        con.execute(f"DELETE FROM users WHERE user_id = '{user_id}'")

        con.commit()

    def delete_user_from_admins_table(self, user_id):
        con = self.create_db()

        con.execute(f"DELETE FROM admins WHERE user_id = '{user_id}'")

        con.commit()

    def get_violator_user_id(self):
        con = self.create_db()

        violator_id = con.execute("SELECT user_id FROM violators").fetchone()[0]

        con.commit()

        return violator_id

    def get_data_from_violators_table(self, violator_id, column_name):
        con = self.create_db()

        data = con.execute(
            f"SELECT {column_name} FROM violators WHERE user_id = {violator_id}").fetchone()[0]

        con.commit()

        return data

    def get_violator_id(self, status):
        con = self.create_db()

        try:
            if status == 'Предупрежден':
                id = con.execute(
                    f"SELECT user_id FROM violators WHERE status = '{status}' AND number_of_complaints > 0 ").fetchone()[0]

                con.commit()

                return id
            else:
                id = con.execute(
                    f"SELECT user_id FROM violators WHERE status = '{status}'").fetchone()[0]

                con.commit()

                return id
        except:
            con.commit()

    # def get_all_violators_id(self):
    #     all_violators_id = self.connector.execute("SELECT * FROM users").fetchall()
    #
    #     list_all_id = []
    #
    #     for i in range(len(all_violators_id)):
    #         list_all_id.append(int(all_violators_id[i][0]))
    #
    #     if len(list_all_id) == 0:
    #         return False
    #     else:
    #         return True

    def update_viewed_ids(self, other_id, self_id):
        con = self.create_db()

        viewed_ids = con.execute(
            f"SELECT viewed_ids FROM users WHERE user_id = '{self_id}'").fetchone()[0]

        if str(viewed_ids) == 'None':
            update = con.execute(
                f"UPDATE users SET viewed_ids = ? WHERE user_id = ?", (other_id, self_id,))
        else:
            if str(other_id) not in viewed_ids.split():
                update = con.execute(
                    f"UPDATE users SET viewed_ids = ? WHERE user_id = ?", (str(viewed_ids) + f' {other_id}', self_id,))

        con.commit()

    # def is_viewed_yet(self, other_id, self_id):
    #     with self.connector:
    #         is_viewd = self.connector.execute(
    #             f"SELECT viewed_ids FROM users WHERE user_id = '{self_id}'").fetchone()[0]
    #
    #         if str(is_viewd).find(str(other_id)) == -1:
    #             return False
    #         else:
    #             return True

    # Добавление данных пользователя в таблицу "users"
    def set_data_in_table(self, colomn_name, value, user_id, table_name):
        con = self.create_db()

        update = con.execute(
            f"UPDATE {table_name} SET {colomn_name} = ? WHERE user_id = ?", (value, user_id,))

        con.commit()

    # Проверка на существование пользователя в таблице с названием,
    # которое ранится в переменной "table_name"
    def is_exist_user_in_db(self, user_id, table_name):
        con = self.create_db()

        try:
            current_id = con.execute(f"SELECT user_id FROM {table_name} WHERE user_id = {user_id}").fetchone()[0]

            con.commit()

            return True

        except:
            return False

    # Получение данных пользователя из таблицы "users"
    def get_data_from_profiles_table(self, colomn_name, user_id):
        con = self.create_db()

        data = con.execute(f"SELECT {colomn_name} FROM users WHERE user_id = '{user_id}'")

        con.commit()

        return data.fetchone()[0]

    def get_data_from_admins_table(self, colomn_name, user_id):
        con = self.create_db()

        data = con.execute(f"SELECT {colomn_name} FROM admins WHERE user_id = '{user_id}'")

        con.commit()

        return data.fetchone()[0]

    # Получение id другого пользователя по схожим параметрам: "город" и "кто нравится"
    def find_other_profiles(self, self_id, self_city, self_opposite):
        con = self.create_db()

        other_gender = ''
        if self_opposite == 'Парни':
            other_gender = 'Я парень'
        elif self_opposite == 'Девушки':
            other_gender = 'Я девушка'
        elif self_opposite == 'Все равно':
            other_gender = None

        self_age = int(DataBaseWork().get_data_from_profiles_table('age', self_id))

        if other_gender == 'Я девушка' or other_gender == 'Я парень':
            others_id_city = con.execute(
                "SELECT user_id, city FROM users WHERE gender = ? AND age >= ? AND age <= ? AND photo_or_video_id != '' AND last_action_time != '' AND inactive != -1 AND age != -1",
                [other_gender, self_age - 3, self_age + 3]).fetchall()
        else:
            others_id_city = con.execute(
                "SELECT user_id, city FROM users WHERE age >= ? AND age <= ? AND photo_or_video_id != '' AND last_action_time != '' AND inactive != -1 AND age != -1",
                [self_age - 3, self_age + 3]).fetchall()

        is_viewed = con.execute(
            f"SELECT viewed_ids FROM users WHERE user_id = '{self_id}'").fetchone()[0]

        con.commit()

        for el in others_id_city:
            if str(el[0]) in is_viewed.split():
                others_id_city.remove(el)

        if len(others_id_city) == 0:
            return None

        buff_id = []
        for el in others_id_city:
            val = self.similarity(self_city, el[1])
            if val >= 0.9 and str(el[0]) not in is_viewed.split():
                if el[0] != self_id:
                    buff_id.append(el[0])

        if len(buff_id) == 0:
            return None
        else:
            return int(buff_id[random.randint(0, len(buff_id) - 1)])

    def similarity(self, s1, s2):
        normalized1 = s1.lower()
        normalized2 = s2.lower()
        matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
        return matcher.ratio()

    # Получение id всех пользователей
    def get_all_users_id(self):
        con = self.create_db()

        all_id = con.execute("SELECT user_id FROM users").fetchall()

        con.commit()

        return len(all_id)

    def update_match_id(self, self__id, other_id):
        last_value = self.get_data_from_profiles_table('match_id', other_id)

        if last_value == '-1':
            self.set_data_in_table('match_id', self__id, other_id, 'users')
        else:
            if str(self__id) not in last_value.split():
                self.set_data_in_table('match_id', last_value + ' ' + str(self__id), other_id, 'users')

    def update_mutual_id(self, self__id, other_id):
        last_value = self.get_data_from_profiles_table('mutual_id', other_id)

        if last_value == '-1':
            self.set_data_in_table('mutual_id', self__id, other_id, 'users')
        else:
            if str(self__id) not in last_value.split():
                self.set_data_in_table('mutual_id', last_value + ' ' + str(self__id), other_id, 'users')

    # Получение id всех пользователей, исходя из заданного ограничения по полу
    def get_all_specific_users_id(self, gender):
        if gender == 'Девушкам':
            gender = 'Я девушка'
        elif gender == 'Парням':
            gender = 'Я парень'

        list_all_specific_users_id = []

        con = self.create_db()

        all_specific_users_id = con.execute(
            f"SELECT user_id FROM users WHERE gender = '{gender}'").fetchall()

        con.commit()

        for i in range(len(all_specific_users_id)):
            list_all_specific_users_id.append(int(all_specific_users_id[i][0]))

        return list_all_specific_users_id

    # Формирование excel файла данными о пользователях
    def read_sql_to_frame(self):
        con = self.create_db()
        df = pd.read_sql_query("SELECT * FROM users", con)

        con.commit()

        df = df.drop(columns=['photo_or_video_id', 'changes', 'is_matched', 'viewed_ids', 'now_check_id', 'match_id', 'last_action_time', 'inactive'])
        df.to_excel('Статистика.xlsx')

    def add_photo_or_video_to_admins(self, user_id, photo_video_id):
        con = self.create_db()

        data = con.execute(f"SELECT photo_video_ids FROM admins WHERE user_id = {user_id}").fetchone()[0]

        con.commit()

        if data == None:
            self.set_data_in_table('photo_video_ids', photo_video_id, user_id, 'admins')

    def is_user_blocked(self, user_id):
        con = self.create_db()

        try:
            status = str(con.execute(
                f"SELECT status FROM violators WHERE user_id = {user_id}").fetchone()[0])

            con.commit()

            if status == 'Заблокирован':
                return True
            else:
                return False
        except:
            return False

    def get_active_users(self):
        con = self.create_db()

        active_users = con.execute(
            f"SELECT user_id FROM users WHERE inactive != -1").fetchall()

        con.commit()

        return len(active_users)

# if __name__ == '__main__':
#     db = DataBaseWork()
#     db.create_table_users()
#     db.create_violators_table()
#     db.create_admins_table()
#     print(len(db.get_all_users_id()))
