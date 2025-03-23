from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import DataBaseWork
from handlers import change_mode

import buttons
from handlers import viewing_questionnaires, create_questionnaire
from aiogram import types, Dispatcher

class MenuState(StatesGroup):
    menu = State()

async def menu_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await menu_module(message)

async def menu_module(msg):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        if msg.text == 'Найти друга':
            await viewing_questionnaires.start_check_profiles(msg)

        elif msg.text == '👤 Мой профиль':
            await create_questionnaire.output_from_profile(msg)

        elif msg.text == '⛑ Проблема с ботом':
            if DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'admins') == True:
                await msg.answer('Если у тебя возникли трудности с ботом, то пиши в поддержку:\n@myster_tgbot',
                                 reply_markup=buttons.menu_admin)
            else:
                await msg.answer('Если у тебя возникли трудности с ботом, то пиши в поддержку:\n@myster_tgbot',
                                 reply_markup=buttons.menu)

        elif msg.text == '⛔ Скрыть анкету':
            DataBaseWork().set_data_in_table('inactive', -1, msg.from_user.id, 'users')

            if DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'admins') == True:
                await msg.answer('\n🫶Надеюсь, что ты отлично провел время и нашел родственную душу благодаря мне\!\n'
                                 '\n'
                                 'К сожалению, твоя анкета больше не\nучаствует в поиске 😢\n'
                                 'Рад был с тобой пообщаться, будет скучно 😥\n'
                                 '\n'
                                 'Но **ТЫ** всегда можешь вернуться 🥳\n'
                                 'Жми __**Найти друга**__ и вперед', parse_mode=types.ParseMode.MARKDOWN_V2,
                                 reply_markup=buttons.menu_admin_close)
            else:
                await msg.answer('\n🫶Надеюсь, что ты отлично провел время и нашел родственную душу благодаря мне\!\n'
                                 '\n'
                                 'К сожалению, твоя анкета больше не\nучаствует в поиске 😢\n'
                                 'Рад был с тобой пообщаться, будет скучно 😥\n'
                                 '\n'
                                 'Но **ТЫ** всегда можешь вернуться 🥳\n'
                                 'Жми __**Найти друга**__ и вперед', parse_mode=types.ParseMode.MARKDOWN_V2,
                                 reply_markup=buttons.menu_close)

        elif msg.text == 'Выбор режима':
            print(DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'admins'))
            if DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'admins') == True:
                await change_mode.change_mode_module(msg)
            else:
                # For non-admin users who somehow access this button
                if DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'admins') == True:
                    await msg.answer('У вас нет доступа к этой функции', reply_markup=buttons.menu_admin)
                else:
                    await msg.answer('У вас нет доступа к этой функции', reply_markup=buttons.menu)


def reg_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(menu_handler, state=MenuState.menu)
    
    # Register the handler for common menu commands on all states
    dp.register_message_handler(menu_handler, lambda message: message.text in 
                               ['Найти друга', '👤 Мой профиль', 'Выбор режима', 
                                '⛔ Скрыть анкету', '⛑ Проблема с ботом'], 
                               state="*")



















    # AgACAgIAAxkBAAEOvAVj34rKx2YtpbGeeMDkw7pUzTxy2AACM8QxG-cAAkvNMWp0ESrTPwEAAwIAA3MAAy4E