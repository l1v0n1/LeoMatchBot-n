from aiogram.dispatcher.filters.state import State, StatesGroup

import buttons
from handlers import viewing_questionnaires, create_questionnaire
from aiogram import types, Dispatcher

class MenuState(StatesGroup):
    menu = State()

async def menu_handler(message: types.Message):
    await menu_module(message)

async def menu_module(msg):
    if msg.text == '💌 Тиндер':
        await viewing_questionnaires.start_check_profiles(msg)
    elif msg.text == '👤 Мой профиль':
        await create_questionnaire.output_from_profile(msg)
    elif msg.text == '🙋‍♀ Поддержка️':
        await msg.answer('Если у тебя возникли трудности, то пиши в поддержку:\n@', reply_markup=buttons.menu)

def reg_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_handler, state=MenuState.menu)