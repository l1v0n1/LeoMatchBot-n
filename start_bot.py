import asyncio
from aiogram import types
from aiogram.utils import exceptions
from aiogram.utils import executor
from create_bot import dp
import buttons
from handlers import viewing_questionnaires, create_questionnaire, menu, admin
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import db

class Main(StatesGroup):
    create_profile = State()
    mode = State()

# @dp.errors_handler(exception=exceptions.BotBlocked)
# async def function_name(exception: exceptions.BotBlocked):
#     print(exception)
#     print('Бот заблокирован юзером')
#     return True

@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    await message.answer('Добро пожаловать в чат-бот «K-тиндер» от CHICKO!'
                         ' Здесь ты познакомишься с любителями корейской культуры и, возможно,'
                         ' найдешь свою родственную душу с такими же интересами!')

    # await asyncio.sleep(5)
    if db.is_exist_user_in_db(message.from_user.id, 'admins') == False:
        db.add_user_in_users_table(message.from_user.id, message.from_user.first_name)
        await message.answer('Давай заполним твой профиль и пойдем знакомиться с другими участниками.')
        await create_questionnaire.start_myprofile_module(message)
    else:
        await change_mode(message)

async def change_mode(msg):
    if db.is_exist_user_in_db(msg.from_user.id, 'admins') == True:
        await Main.mode.set()
        await msg.answer('Выберите режим!', reply_markup=buttons.mode)
    else:
        await create_questionnaire.output_from_profile(msg)

@dp.message_handler(state=Main.mode)
async def change_mode_handler(message: types.Message):
    if message.text == 'Администратор':
        await admin.AdminStates.admin_menu.set()
        await admin.admin_menu_module(message)
    elif message.text == 'Обычный пользователь':
        await create_questionnaire.output_from_profile(message)
    else:
        await message.answer('Нет такого варианта ответа!')


if __name__ == '__main__':
    db.create_db()
    db.create_table_users()
    db.create_admins_table()

    viewing_questionnaires.reg_handlers_questionnaire(dp=dp)
    create_questionnaire.reg_handlers_questionnaire(dp=dp)
    menu.reg_menu_handlers(dp=dp)
    admin.reg_handlers_questionnaire(dp=dp)

    executor.start_polling(dp, skip_updates=True)
