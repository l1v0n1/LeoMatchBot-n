import sqlite3

from create_bot import bot, types
from work_with_db import DataBaseWork
import asyncio
import time

DataBaseWork().create_table_users()
DataBaseWork().create_violators_table()
DataBaseWork().create_admins_table()

async def check_activity():
    while True:
        try:
            try:
                users_ids = DataBaseWork().get_all_users_id()
                for user_id in users_ids:
                    last_time = DataBaseWork().get_data_from_profiles_table('last_action_time', user_id)
                    user_activity = DataBaseWork().get_data_from_profiles_table('inactive', user_id)
                    if last_time != '' and user_activity == 0:
                        if float(time.time()) - float(last_time) >= float(2.628*10**6):
                            DataBaseWork().set_data_in_table('inactive', -1, user_id, 'users')
                            DataBaseWork().set_data_in_table('last_action_time', time.time(), user_id, 'users')
                            await bot.send_message(user_id, 'Привет\! От тебя давно не было активности, '
                                                            'поэтому твоя анкета больше не участвует в поиске\.\n'
                                                            '\n'
                                                            'Для возвращения прояви активность\.\n'
                                                            '\n'
                                                            'Может начнем все сначала?\n'
                                                            '\n'
                                                            'Жми __**Найти друга**__ и вперед', parse_mode=types.ParseMode.MARKDOWN_V2)
                time.sleep(float(60*60*24))
            except sqlite3.Error:
                continue
        except Exception:
            continue
                # elif last_time != '' and user_activity == -1:
                #     if float(time.time()) - float(last_time) >= 20:
                #         db.set_data_in_table('last_action_time', time.time(), user_id, 'users')
                #         print('send_message2')
                #         # db.delete_user_from_users_table(user_id)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_activity())
