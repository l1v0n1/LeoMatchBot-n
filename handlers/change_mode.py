import buttons
import start_bot
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import DataBaseWork
from aiogram.dispatcher.filters import Text
from handlers import create_questionnaire, admin

class ChangeMode(StatesGroup):
    mode = State()

async def change_mode_module(msg):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        if DataBaseWork().is_exist_user_in_db(msg.from_user.id, 'admins') == True:
            await ChangeMode.mode.set()
            await msg.answer('Выберите режим!', reply_markup=buttons.mode)
        else:
            await create_questionnaire.output_from_profile(msg)

# @dp.message_handler(state=ChangeMode.mode)
async def change_mode_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        if message.text == 'Администратор':
            await admin.AdminStates.admin_menu.set()
            await admin.admin_menu_module(message)
        elif message.text == 'Обычный пользователь':
            if DataBaseWork().is_exist_user_in_db(message.from_user.id, 'users') == False:
                await message.answer('Давай заполним твой профиль и пойдем знакомиться с другими участниками.')
                if message.from_user.username == None:
                    await message.answer('Для взаимодействия с ботом необходимо задать Username '
                                         'в настройках Telegram после чего нажать\n'
                                         '/start')

                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo='AgACAgIAAxkBAAMGY9Z6dOyfyJdbmI09Bcv9RaKpoLQAAvPEMRtpIrBKOIZmG3Iqn9cBAAMCAANzAAMtBA',
                                         caption='IOS\n\n'
                                                 '1. Нажмите ⚙️Настройки в правом нижнем углу\n'
                                                 '2. Нажмите "Выбрать имя пользователя"\n'
                                                 '3. Введите имя пользователя')
                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo='AgACAgIAAxkBAAMFY9Z6XwceJQUsZWmf4o6uLl-c-SIAAvHEMRtpIrBKWONeyvTHVCwBAAMCAANzAAMtBA',
                                         caption='Android\n\n'
                                                 '1. Нажмите на 3 полоски в левом верхнем углу\n'
                                                 '2. Нажмите ⚙️Настройки\n'
                                                 '3. Нажмите на "Имя пользователя" и введите имя')
                else:
                    DataBaseWork().add_user_in_users_table(message.from_user.id, message.from_user.username)
                    await create_questionnaire.start_myprofile_module(message)
            else:
                if DataBaseWork().get_data_from_profiles_table('photo_or_video_id', message.from_user.id) == '':
                    await create_questionnaire.start_myprofile_module(message)
                else:
                    await create_questionnaire.output_from_profile(message)
        else:
            await message.answer('Нет такого варианта ответа!')

def reg_handlers_change_mode(dp: Dispatcher):
    dp.register_message_handler(change_mode_handler, state=ChangeMode.mode)

