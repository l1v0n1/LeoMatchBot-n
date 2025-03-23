import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import DataBaseWork
from aiogram.dispatcher.filters import Text
from handlers import viewing_questionnaires, menu, change_mode
import start_bot

class Match(StatesGroup):
    match = State()
    yes_no = State()

async def send_notification_about_matching_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await send_notification_about_matching_module(message)

async def send_notification_about_matching_module(msg):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        who_liked_me_id = DataBaseWork().get_data_from_profiles_table('match_id', msg.from_user.id)
        
        # If no matches found, go to profile viewing
        if who_liked_me_id is None or who_liked_me_id == '-1':
            return await viewing_questionnaires.start_check_profiles(msg)

        # Check each match
        filtered_ids = []
        for el in who_liked_me_id.split():
            print(el, type(el))
            photo_id = DataBaseWork().get_data_from_profiles_table('photo_or_video_id', el)
            if photo_id is None or photo_id == '':
                # Skip this match, but keep processing others
                continue
            filtered_ids.append(el)
        
        # If all matches were invalid, reset and go to profile viewing
        if not filtered_ids:
            DataBaseWork().set_data_in_table('match_id', '-1', msg.from_user.id, 'users')
            return await viewing_questionnaires.start_check_profiles(msg)
        
        # Update the match list with valid matches only
        new_who_liked_me_id = ' '.join(filtered_ids)
        DataBaseWork().set_data_in_table('match_id', new_who_liked_me_id, msg.from_user.id, 'users')

        try:
            DataBaseWork().set_data_in_table('is_matched', True, msg.from_user.id, 'users')

            await bot.send_message(chat_id=msg.from_user.id,
                                   text=f'Вы понравились {len(filtered_ids)} '
                                        f'пользователю(-ям)!\nПосмотреть анкету(-ы)?',
                                   reply_markup=buttons.da_net)
            await Match.yes_no.set()
        except Exception as e:
            print(f'Исключение в match.py для юзера с id = {msg.from_user.id}: {e}')

# Обработчик кнопок "да" и "нет", которые выводятся с сообщением "Вы понравились пользователю!
# Посмотреть анкету?"
async def yes_no_match(callback: types.CallbackQuery):
    if DataBaseWork().is_user_blocked(callback.from_user.id) == False:
        try:
            if callback.data == 'yes_show_me':
                # who_liked_me_id = DataBaseWork().get_data_from_profiles_table('match_id', callback.from_user.id)
                await viewing_questionnaires.CheckProfiles.reaction.set()
                await viewing_questionnaires.output_from_profile(callback.from_user.id)
                # await viewing_questionnaires.output_from_profile(callback.from_user.id, True, who_liked_me_id.split()[0])
            elif callback.data == 'dont_show_me':
                DataBaseWork().set_data_in_table('is_matched', False, callback.from_user.id, 'users')
                DataBaseWork().set_data_in_table('match_id', '-1', callback.from_user.id, 'users')

                await viewing_questionnaires.CheckProfiles.reaction.set()

                await viewing_questionnaires.output_from_profile(callback.from_user.id)
        except:
            print('Кнопки "да или нет" не сработали')

async def is_menu(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        if message.text in ['Найти друга', '👤 Мой профиль', 'Выбор режима', '⛔ Скрыть анкету', '⛑ Проблема с ботом']:
            await menu.menu_module(message)
        elif message.text == '/start':
            await start_bot.command_start_module(message)

def reg_handlers_match(dp: Dispatcher):
    dp.register_message_handler(send_notification_about_matching_handler, state=Match.match)
    dp.register_callback_query_handler(yes_no_match, state=Match.yes_no)
    dp.register_callback_query_handler(is_menu, state=Match.all_states)
