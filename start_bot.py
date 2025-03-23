import asyncio
from aiogram import types
from aiogram.utils import executor
from work_with_db import DataBaseWork
from create_bot import dp, bot
import buttons
from handlers import viewing_questionnaires, create_questionnaire, menu, admin, change_mode, match
from aiogram.dispatcher.filters.state import State, StatesGroup
from threading import Thread, Event
import time
import sqlite3

class StartStates(StatesGroup):
    sleep = State()

# @dp.message_handler(commands='start')
# async def command_start(message: types.Message):
#     await command_start_module(message)

async def command_start_module(msg):
    if DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'admins') == False:
        if DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'users') == False:
            await msg.answer('Давай заполним твой профиль и пойдем знакомиться с другими участниками.')

            if msg.from_user.username == None:
                await msg.answer('Для взаимодействия с ботом необходимо задать Username '
                                     'в настройках Telegram после чего нажать\n'
                                     '/start')

                
                await bot.send_message(chat_id=msg.from_user.id,
                                       text='IOS\n\n'
                                             '1. Нажмите ⚙️Настройки в правом нижнем углу\n'
                                             '2. Нажмите "Выбрать имя пользователя"\n'
                                             '3. Введите имя пользователя\n\n'
                                             'Android\n\n'
                                             '1. Нажмите на 3 полоски в левом верхнем углу\n'
                                             '2. Нажмите ⚙️Настройки\n'
                                             '3. Нажмите на "Имя пользователя" и введите имя')

            else:
                DataBaseWork().add_user_in_users_table(msg.from_user.id, msg.from_user.username)
                await create_questionnaire.start_myprofile_module(msg)
        else:
            if DataBaseWork().get_data_from_profiles_table('photo_or_video_id', msg.from_user.id) == '':
                await create_questionnaire.start_myprofile_module(msg)
            else:
                await create_questionnaire.output_from_profile(msg)
    else:
        await change_mode.change_mode_module(msg)

# Если пользователь уже пользовался ботом и бот был перезапущен, то данный
# хендлер вернет его в command_start_module(msg)
@dp.message_handler()
async def arbitrary_start(message: types.Message):
    await message.answer('Добро пожаловать в чат-бот для знакомств!\n'
                        'Здесь ты познакомишься с интересными людьми и, возможно,'
                        ' найдешь свою вторую половинку!')
    await command_start_module(message)

# Проверка активных пользователей
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
                                                            'поэтому твоя анкета больше не участвует в поиске\.😲\n'
                                                            '\n'
                                                            '❤️‍🔥Для возвращения прояви активность\.👈\n'
                                                            '\n'
                                                            'Может начнем все сначала?\n'
                                                            '\n'
                                                            'Жми __**🫰🏼Найти друга**__ и вперед🫰', parse_mode=types.ParseMode.MARKDOWN_V2)
                time.sleep(float(60*60*24))
            except sqlite3.Error:
                continue
        except Exception:
            continue

if __name__ == '__main__':
    DataBaseWork().create_table_users()
    DataBaseWork().create_admins_table()
    DataBaseWork().create_violators_table()
    
    # Initialize admins from config
    import config
    for admin_id in config.admin_id:
        if not DataBaseWork().is_exist_user_in_db(admin_id, 'admins'):
            print(f"Adding admin with ID {admin_id} to the database")
            DataBaseWork().add_user_in_admins_table(admin_id)

    change_mode.reg_handlers_change_mode(dp=dp)
    viewing_questionnaires.reg_handlers_questionnaire(dp=dp)
    create_questionnaire.reg_handlers_questionnaire(dp=dp)
    menu.reg_menu_handlers(dp=dp)
    admin.reg_handlers_questionnaire(dp=dp)
    match.reg_handlers_match(dp=dp)

    executor.start_polling(dp, skip_updates=True)
    loop = asyncio.get_event_loop()
    loop.create_task(check_activity())