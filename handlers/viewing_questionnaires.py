import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from start_bot import DataBaseWork
from handlers import create_questionnaire, menu, match
import time
import start_bot

class CheckProfiles(StatesGroup):
    check = State()
    reaction = State()
    sleep = State()
    waiting = State()

async def is_change_user_name(msg):
    return DataBaseWork().set_data_in_table('user_nickname', msg.from_user.username, msg.from_user.id, 'users')

async def start_check_profiles_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await start_check_profiles(message)

async def start_check_profiles(msg):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        await is_change_user_name(msg)

        match_id = DataBaseWork().get_data_from_profiles_table('match_id', msg.from_user.id)
        if match_id is None:
            match_id = '-1'
            DataBaseWork().set_data_in_table('match_id', match_id, msg.from_user.id, 'users')
        
        if match_id != '-1':
            await match.send_notification_about_matching_module(msg)
        else:
            is_matched = DataBaseWork().get_data_from_profiles_table('is_matched', msg.from_user.id)
            if is_matched is None:
                is_matched = False
                DataBaseWork().set_data_in_table('is_matched', is_matched, msg.from_user.id, 'users')
                
            if is_matched == True:
                DataBaseWork().set_data_in_table('is_matched', False, msg.from_user.id, 'users')

            await CheckProfiles.reaction.set()
            await output_from_profile(msg.from_user.id)

async def output_from_profile(self_id):
    if DataBaseWork().is_user_blocked(self_id) == False:
        if DataBaseWork().is_exist_user_in_db(self_id, 'admins') == True:
            await bot.send_message(chat_id=self_id, text='🔍', reply_markup=buttons.menu_admin)
        else:
            await bot.send_message(chat_id=self_id, text='🔍', reply_markup=buttons.menu)

        other_id = 0
        
        is_matched = DataBaseWork().get_data_from_profiles_table('is_matched', self_id)
        if is_matched is None:
            is_matched = False
            DataBaseWork().set_data_in_table('is_matched', is_matched, self_id, 'users')

        if is_matched == False:
            now_check_id = DataBaseWork().get_data_from_profiles_table('now_check_id', self_id)
            if now_check_id is None:
                now_check_id = -1
                
            viewed_ids = DataBaseWork().get_data_from_profiles_table('viewed_ids', self_id)
            if viewed_ids is None:
                viewed_ids = ''
                
            if f"{now_check_id}" not in viewed_ids.split() and now_check_id != -1:
                other_id = now_check_id
            else:
                # Find other profiles based on matching criteria
                other_id = DataBaseWork().find_other_profiles(
                    self_id,
                    DataBaseWork().get_data_from_profiles_table('city', self_id),
                    DataBaseWork().get_data_from_profiles_table('opposite', self_id))

                if other_id is None:
                    if DataBaseWork().is_exist_user_in_db(self_id, 'admins') == True:
                        await bot.send_message(self_id,
                                               'Анкет, похожих на твою, пока нет!',
                                               reply_markup=buttons.menu_admin)
                    else:
                        await bot.send_message(self_id,
                                               'Анкет, похожих на твою, пока нет!',
                                               reply_markup=buttons.menu)

                    DataBaseWork().set_data_in_table('last_action_time', time.time(), self_id, 'users')
                    DataBaseWork().set_data_in_table('inactive', 0, self_id, 'users')

                    await CheckProfiles.sleep.set()

                    return

                DataBaseWork().set_data_in_table('now_check_id', other_id, self_id, 'users')
        else:
            match_id = DataBaseWork().get_data_from_profiles_table('match_id', self_id)
            if match_id is None or match_id == '-1':
                # No matches, reset state
                DataBaseWork().set_data_in_table('is_matched', False, self_id, 'users')
                await bot.send_message(self_id, 'Анкеты закончились!', reply_markup=buttons.menu)
                return
                
            other_id = match_id.split()[-1]

        photo_or_video_id = DataBaseWork().get_data_from_profiles_table('photo_or_video_id', other_id)
        if photo_or_video_id is None:
            # Handle missing media, skip to next profile
            DataBaseWork().update_viewed_ids(other_id, self_id)
            await output_from_profile(self_id)
            return
            
        # Get user data safely
        user_name = DataBaseWork().get_data_from_profiles_table('user_name', other_id)
        if user_name is None: user_name = ""
        
        age = DataBaseWork().get_data_from_profiles_table('age', other_id)
        if age is None: age = ""
        
        city = DataBaseWork().get_data_from_profiles_table('city', other_id)
        if city is None: city = ""
        
        description = DataBaseWork().get_data_from_profiles_table('description', other_id)
        if description is None: description = ""
        
        dop_info = DataBaseWork().get_data_from_profiles_table('dop_info', other_id)
        if dop_info is None: dop_info = ""

        if description == '':
            data = f"{user_name}, {age}, {city}.\n\n{dop_info}"
        else:
            data = f"{user_name}, {age}, {city} - {description}.\n\n{dop_info}"

        data = await correctness_profile_text(data)

        try:
            try:
                try:
                    await bot.send_photo(chat_id=self_id, photo=photo_or_video_id, caption=data,
                                         reply_markup=buttons.inline_markup)
                except:
                    await bot.send_video(chat_id=self_id, video=photo_or_video_id, caption=data,
                                         reply_markup=buttons.inline_markup)
            except:
                print('Ошибка при отправке медиафайла')
                DataBaseWork().update_viewed_ids(other_id, self_id)
                return await output_from_profile(self_id)

        except:
            pass

        DataBaseWork().set_data_in_table('last_action_time', time.time(), self_id, 'users')
        DataBaseWork().set_data_in_table('inactive', 0, self_id, 'users')

async def is_plus(callback: types.CallbackQuery):
    if DataBaseWork().is_user_blocked(callback.from_user.id) == False:
        await is_change_user_name(callback)

        await callback.message.answer('👍')
        
        # Get the ID of the user being liked
        current_profile_id = DataBaseWork().get_data_from_profiles_table('now_check_id', callback.from_user.id)
        if current_profile_id is None:
            # Handle case when profile ID is not found
            await output_from_profile(callback.from_user.id)
            return
        
        # Check if the current profile already liked this user
        other_user_match_ids = DataBaseWork().get_data_from_profiles_table('match_id', current_profile_id)
        if other_user_match_ids is None:
            # Handle case when match_id is not found
            other_user_match_ids = '-1'
        
        # If the other user has already liked this user, trigger a match immediately
        if str(callback.from_user.id) in other_user_match_ids.split():
            # Set match state for both users
            DataBaseWork().set_data_in_table('is_matched', True, callback.from_user.id, 'users')
            DataBaseWork().set_data_in_table('is_matched', True, current_profile_id, 'users')
            
            # Add to match_id list
            match_id = DataBaseWork().get_data_from_profiles_table('match_id', callback.from_user.id)
            if match_id is None or match_id == '-1':
                DataBaseWork().set_data_in_table('match_id', str(current_profile_id), callback.from_user.id, 'users')
            else:
                DataBaseWork().set_data_in_table('match_id', match_id + ' ' + str(current_profile_id), callback.from_user.id, 'users')
            
            # Update mutual IDs
            DataBaseWork().update_mutual_id(callback.from_user.id, current_profile_id)
            DataBaseWork().update_mutual_id(current_profile_id, callback.from_user.id)
            
            # Send match notifications immediately
            try:
                await bot.send_message(
                    chat_id=callback.from_user.id,
                    text=f'💌 Случился мэтч! '
                            f'Нажми на кнопку ниже, чтобы увидеть контакты или нажми кнопку Найти друга, чтобы '
                            f'продолжить подбор анкет!\n', reply_markup=buttons.view_markup)
            except Exception as ex:
                print('ошибка с фото\n\n', ex)
                
                
            try:
                await bot.send_message(
                    chat_id=current_profile_id,
                    text=f'💌 Случился мэтч! '
                            f'Нажми на кнопку ниже, чтобы увидеть контакты или нажми кнопку Найти друга, чтобы '
                            f'продолжить подбор анкет!\n', reply_markup=buttons.view_markup)
                # Set state for other user
                state = dp.current_state(chat=current_profile_id, user=current_profile_id)
                await state.set_state(CheckProfiles.waiting)
            except Exception as ex:
                print('ошибка с фото\n\n', ex)
                
            await CheckProfiles.waiting.set()
            
            # Remove from each other's match_id lists since we already notified them
            DataBaseWork().set_data_in_table('match_id', '-1', callback.from_user.id, 'users')
            DataBaseWork().update_viewed_ids(current_profile_id, callback.from_user.id)
        
        elif DataBaseWork().get_data_from_profiles_table('is_matched', callback.from_user.id) == True:
            # Original match notification logic for existing matches
            all_matches = DataBaseWork().get_data_from_profiles_table('match_id', callback.from_user.id)

            try:
                try:
                    await bot.send_message(
                        chat_id=callback.from_user.id,
                        text=f'💌 Случился мэтч! '
                                f'Нажми на кнопку ниже, чтобы увидеть контакты или нажми кнопку Найти друга, чтобы '
                                f'продолжить подбор анкет!\n', reply_markup=buttons.view_markup)
                except Exception as ex:
                    print('ошибка с фото\n\n', ex)
                try:
                    await bot.send_message(
                        chat_id=all_matches.split()[-1],
                        text=f'💌 Случился мэтч! '
                                f'Нажми на кнопку ниже, чтобы увидеть контакты или нажми кнопку Найти друга, чтобы '
                                f'продолжить подбор анкет!\n', reply_markup=buttons.view_markup)
                    state = dp.current_state(chat=all_matches.split()[-1],
                                             user=all_matches.split()[-1])
                    await state.set_state(CheckProfiles.waiting)
                except Exception as ex:
                    print('ошибка с фото\n\n', ex)

            except Exception as ex:
                print('общая ошибка\n\n', ex)

            await CheckProfiles.waiting.set()

            DataBaseWork().update_mutual_id(all_matches.split()[-1], callback.from_user.id)
            DataBaseWork().update_mutual_id(callback.from_user.id, all_matches.split()[-1])

            if len(all_matches.split()) == 1:
                all_matches = '-1'
                DataBaseWork().set_data_in_table('match_id', all_matches, callback.from_user.id, 'users')
            elif len(all_matches.split()) > 1:
                index = all_matches.find(f'{all_matches.split()[-1]}')
                all_matches = all_matches[:index - 1]
                DataBaseWork().set_data_in_table('match_id', all_matches, callback.from_user.id, 'users')
        else:
            # Just store the like and continue as before
            DataBaseWork().update_match_id(callback.from_user.id,
                               DataBaseWork().get_data_from_profiles_table('now_check_id', callback.from_user.id))

            DataBaseWork().update_viewed_ids(DataBaseWork().get_data_from_profiles_table('now_check_id', callback.from_user.id), callback.from_user.id)

            await CheckProfiles.check.set()
            await start_check_profiles(callback)

async def is_minus(callback: types.CallbackQuery):
    if DataBaseWork().is_user_blocked(callback.from_user.id) == False:
        await is_change_user_name(callback)

        await callback.message.answer('👎')

        all_matches = DataBaseWork().get_data_from_profiles_table('match_id', callback.from_user.id)

        if DataBaseWork().get_data_from_profiles_table('is_matched', callback.from_user.id) == True:
            DataBaseWork().update_viewed_ids(all_matches.split()[-1], callback.from_user.id)

            if len(all_matches.split()) == 1:
                all_matches = -1
                DataBaseWork().set_data_in_table('match_id', all_matches, callback.from_user.id, 'users')

            elif len(all_matches.split()) > 1:
                index = all_matches.find(f'{all_matches.split()[-1]}')
                all_matches = all_matches[:index - 1]
                DataBaseWork().set_data_in_table('match_id', all_matches, callback.from_user.id, 'users')
        else:
            DataBaseWork().update_viewed_ids(
                DataBaseWork().get_data_from_profiles_table(
                    'now_check_id', callback.from_user.id),
                callback.from_user.id)

        await CheckProfiles.check.set()
        await start_check_profiles(callback)

async def is_complain(callback: types.CallbackQuery):
    if DataBaseWork().is_user_blocked(callback.from_user.id) == False:
        await is_change_user_name(callback)

        all_matches = DataBaseWork().get_data_from_profiles_table('match_id', callback.from_user.id)
        if all_matches is None:
            all_matches = '-1'

        is_matched = DataBaseWork().get_data_from_profiles_table('is_matched', callback.from_user.id)
        if is_matched is None:
            is_matched = False

        if is_matched == True and all_matches != '-1':
            # Handle matched user complaint
            try:
                match_id = all_matches.split()[-1]
                DataBaseWork().update_viewed_ids(match_id, callback.from_user.id)
                DataBaseWork().add_user_in_violators_table(match_id)

                # Update match list
                if len(all_matches.split()) > 1:
                    index = all_matches.rfind(' ')
                    all_matches = all_matches[:index]
                else:
                    all_matches = '-1'
                
                DataBaseWork().set_data_in_table('match_id', all_matches, callback.from_user.id, 'users')
            except Exception as e:
                print(f"Error in is_complain for matched user: {e}")
                DataBaseWork().set_data_in_table('match_id', '-1', callback.from_user.id, 'users')
        else:
            # Handle regular complaint
            now_check_id = DataBaseWork().get_data_from_profiles_table('now_check_id', callback.from_user.id)
            if now_check_id is not None:
                DataBaseWork().update_viewed_ids(now_check_id, callback.from_user.id)
                DataBaseWork().add_user_in_violators_table(now_check_id)

        await callback.message.answer('Жалоба отправлена!')
        await CheckProfiles.check.set()
        await start_check_profiles(callback)

async def is_view_match_profile(callback: types.CallbackQuery):
    if DataBaseWork().is_user_blocked(callback.from_user.id) == False:
        await is_change_user_name(callback)

        mutual_id = DataBaseWork().get_data_from_profiles_table('mutual_id', callback.from_user.id)
        if mutual_id is None or mutual_id == '-1':
            await callback.message.answer('Нет взаимных лайков!')
            return
            
        list_osther_id = mutual_id.split()

        if list_osther_id[0] != '-1':
            try:
                other_id = int(list_osther_id[-1])

                photo_or_video_id = DataBaseWork().get_data_from_profiles_table('photo_or_video_id', other_id)
                if photo_or_video_id is None:
                    # Handle case when photo_or_video_id is not found
                    await callback.message.answer('Информация о профиле недоступна')
                    return

                if DataBaseWork().get_data_from_profiles_table('description', other_id) == '':
                    data = f"{DataBaseWork().get_data_from_profiles_table('user_name', other_id)}, " \
                          f"{DataBaseWork().get_data_from_profiles_table('age', other_id)}, " \
                          f"{DataBaseWork().get_data_from_profiles_table('city', other_id)}.\n\n" \
                          f"{DataBaseWork().get_data_from_profiles_table('dop_info', other_id)}"

                else:
                    data = f"{DataBaseWork().get_data_from_profiles_table('user_name', other_id)}, " \
                          f"{DataBaseWork().get_data_from_profiles_table('age', other_id)}, " \
                          f"{DataBaseWork().get_data_from_profiles_table('city', other_id)} - " \
                          f"{DataBaseWork().get_data_from_profiles_table('description', other_id)}.\n\n" \
                          f"{DataBaseWork().get_data_from_profiles_table('dop_info', other_id)}"

                data = await correctness_profile_text(data)

                data = data + f'\n\nКонтакты: @{DataBaseWork().get_data_from_profiles_table("user_nickname", other_id)}'

                try:
                    try:
                        await bot.send_photo(chat_id=callback.from_user.id, photo=photo_or_video_id, caption=data)
                    except:
                        await bot.send_video(chat_id=callback.from_user.id, video=photo_or_video_id, caption=data)
                except:
                    pass

                all_mutuals = DataBaseWork().get_data_from_profiles_table('mutual_id', callback.from_user.id)  #'312213 123123 21321'   ['312213' '123123' '21321']

                if len(all_mutuals.split()) > 1:
                    index = all_mutuals.find(f'{all_mutuals.split()[-1]}')
                    all_mutuals = all_mutuals[:index-1]
                elif len(all_mutuals.split()) == 1:
                    all_mutuals = '-1'

                DataBaseWork().set_data_in_table('mutual_id', all_mutuals, callback.from_user.id, 'users')
            except Exception as ex:
                print('Ошибка при обработке данных', ex)
        else:
            await callback.message.answer('Анкеты людей, с которыми у тебя случился мэтч, закончились!')

        if DataBaseWork().is_exist_user_in_db(callback.from_user.id, 'admins') == True:
            await callback.message.answer('Чтобы продолжить знакомство с людьми, нажми Найти друга', reply_markup=buttons.menu_admin)
        else:
            await callback.message.answer('Чтобы продолжить знакомство с людьми, нажми Найти друга', reply_markup=buttons.menu)

async def correctness_profile_text(profile_text):
    if len(profile_text) > 990:
        profile_text = profile_text[0:990]
        profile_text += ' ...'

    return profile_text

async def is_menu(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text in ['Найти друга', '👤 Мой профиль', 'Выбор режима', '⛔ Скрыть анкету', '⛑ Проблема с ботом']:
            await menu.menu_module(message)
        elif message.text == '/start':
            await start_bot.command_start_module(message)

def reg_handlers_questionnaire(dp: Dispatcher):
    dp.register_message_handler(start_check_profiles_handler)
    dp.register_callback_query_handler(is_plus, Text('👍'), state=CheckProfiles.reaction)
    dp.register_callback_query_handler(is_minus, Text('👎'), state=CheckProfiles.reaction)
    dp.register_callback_query_handler(is_complain, Text('complain'), state=CheckProfiles.reaction)
    dp.register_callback_query_handler(is_view_match_profile, Text('view'), state=CheckProfiles.all_states)
    dp.register_message_handler(is_menu, state=CheckProfiles.all_states)