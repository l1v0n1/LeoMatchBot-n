import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from start_bot import db
from handlers import create_questionnaire, menu

class CheckProfiles(StatesGroup):
    check = State()
    reaction = State()
    sleep = State()

async def start_check_profiles_handler(message: types.Message):
    await start_check_profiles(message)

async def start_check_profiles(msg):
    await CheckProfiles.reaction.set()
    await bot.send_message(chat_id=msg.from_user.id, text='✨🔍', reply_markup=buttons.menu)
    await output_from_profile(msg.from_user.id)

async def output_from_profile(self_id):
    other_id = db.find_other_profiles(self_id,
                                      db.get_data_from_profiles_table('city', self_id),
                                      db.get_data_from_profiles_table('gender', self_id))
    photo_or_video_id = db.get_data_from_profiles_table('photo_or_video_id', other_id)

    if db.get_data_from_profiles_table('description', other_id) == '':
        str = f"{db.get_data_from_profiles_table('user_name', other_id)}, " \
              f"{db.get_data_from_profiles_table('age', other_id)}, " \
              f"{db.get_data_from_profiles_table('city', other_id)}." \
              f"{db.get_data_from_profiles_table('dop_info', other_id)}"

    else:
        str = f"{db.get_data_from_profiles_table('user_name', other_id)}, " \
              f"{db.get_data_from_profiles_table('age', other_id)}, " \
              f"{db.get_data_from_profiles_table('city', other_id)} - " \
              f"{db.get_data_from_profiles_table('description', other_id)}.\n" \
              f"{db.get_data_from_profiles_table('dop_info', other_id)}"


    try:
        await bot.send_photo(chat_id=self_id, photo=photo_or_video_id, caption=str, reply_markup=buttons.inline_markup)

    except:
        await bot.send_video(chat_id=self_id,video=photo_or_video_id, caption=str, reply_markup=buttons.inline_markup)

async def is_plus(callback: types.CallbackQuery):
    await CheckProfiles.check.set()
    await start_check_profiles(callback)

async def is_minus(callback: types.CallbackQuery):
    await CheckProfiles.check.set()
    await start_check_profiles(callback)

async def is_menu(message: types.Message):
    if message.text in ['💌 Тиндер', '👤 Мой профиль', '🙋‍♀ Поддержка️']:
        await menu.MenuState.menu.set()
        await menu.menu_module(message)

def reg_handlers_questionnaire(dp: Dispatcher):
    dp.register_message_handler(start_check_profiles_handler)
    dp.register_callback_query_handler(is_plus, Text('👍'), state=CheckProfiles.reaction)
    dp.register_callback_query_handler(is_minus, Text('👎'), state=CheckProfiles.reaction)
    dp.register_message_handler(is_menu, state=CheckProfiles.reaction)