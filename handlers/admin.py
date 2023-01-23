import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import db

class AdminStates(StatesGroup):
    admin_menu = State()

async def admin_menu_handler(message: types.Message):
    await admin_menu_module(message)

async def admin_menu_module(msg):
    if db.get_data_from_profiles_table('is_admin', msg.from_user.id) == True:
        await msg.answer('Привет, хозяин!')

def reg_handlers_questionnaire(dp: Dispatcher):
    dp.register_message_handler(admin_menu_handler, commands='admin', state=AdminStates.admin_menu)