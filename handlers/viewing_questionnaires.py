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

        if DataBaseWork().get_data_from_profiles_table('match_id', msg.from_user.id) != '-1':
            await match.send_notification_about_matching_module(msg)
        else:
            if DataBaseWork().get_data_from_profiles_table('is_matched', msg.from_user.id) == True:
                DataBaseWork().set_data_in_table('is_matched', False, msg.from_user.id, 'users')

            await CheckProfiles.reaction.set()
            await output_from_profile(msg.from_user.id)

async def output_from_profile(self_id):
    if DataBaseWork().is_user_blocked(self_id) == False:
        if DataBaseWork().is_exist_user_in_db(self_id, 'admins') == True:
            await bot.send_message(chat_id=self_id, text='✨🔍', reply_markup=buttons.menu_admin)
        else:
            await bot.send_message(chat_id=self_id, text='✨🔍', reply_markup=buttons.menu)

        other_id = 0

        print('ыыы')
        print(type(DataBaseWork().get_data_from_profiles_table('now_check_id', self_id)))

        if DataBaseWork().get_data_from_profiles_table('is_matched', self_id) == False:
            if f"{DataBaseWork().get_data_from_profiles_table('now_check_id', self_id)}" not in DataBaseWork().get_data_from_profiles_table('viewed_ids', self_id).split() and \
                    DataBaseWork().get_data_from_profiles_table('now_check_id', self_id) != -1:
                other_id = DataBaseWork().get_data_from_profiles_table('now_check_id', self_id)
                # print('4444')
            else:
                other_id = DataBaseWork().find_other_profiles(
                    self_id,
                    DataBaseWork().get_data_from_profiles_table('city', self_id),
                    DataBaseWork().get_data_from_profiles_table('opposite', self_id))

                if other_id == None:
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
            #     print('3333')
            # print('11111111111')
        else:
            other_id = (DataBaseWork().get_data_from_profiles_table('match_id', self_id)).split()[-1]

        photo_or_video_id = DataBaseWork().get_data_from_profiles_table('photo_or_video_id', other_id)

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

        try:
            try:
                try:
                    await bot.send_photo(chat_id=self_id, photo=photo_or_video_id, caption=data,
                                         reply_markup=buttons.inline_markup)
                except:
                    await bot.send_video(chat_id=self_id, video=photo_or_video_id, caption=data,
                                         reply_markup=buttons.inline_markup)
            except:
                print('haha, pidor')
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

        if DataBaseWork().get_data_from_profiles_table('is_matched', callback.from_user.id) == True:
            all_matches = DataBaseWork().get_data_from_profiles_table('match_id', callback.from_user.id)

            try:
                try:
                    await bot.send_photo(
                        chat_id=callback.from_user.id,
                        photo='AgACAgIAAxkBAAIO82PYBOEl0c9YQf5hONt9ZJj3AwmSAAK0yTEbeFnBSrmK4zN5a0yHAQADAgADcwADLQQ',
                        caption=f'💌 Случился мэтч! '
                                f'Нажми на кнопку ниже, чтобы увидеть контакты или нажми кнопку 🫰🏼Найти друга, чтобы '
                                f'продолжить подбор анкет!\n', reply_markup=buttons.view_markup)
                except Exception as ex:
                    print('ошибка с фото\n\n', ex)
                try:
                    await bot.send_photo(
                        chat_id=all_matches.split()[-1],
                        photo='AgACAgIAAxkBAAIO82PYBOEl0c9YQf5hONt9ZJj3AwmSAAK0yTEbeFnBSrmK4zN5a0yHAQADAgADcwADLQQ',
                        caption=f'💌 Случился мэтч! '
                                f'Нажми на кнопку ниже, чтобы увидеть контакты или нажми кнопку 🫰🏼Найти друга, чтобы '
                                f'продолжить подбор анкет!\n', reply_markup=buttons.view_markup)
                    state = dp.current_state(chat=all_matches.split()[-1],
                                             user=all_matches.split()[-1])
                    await state.set_state(CheckProfiles.waiting)
                except Exception as ex:
                    print('ошибка с видео\n\n', ex)

            except Exception as ex:
                print('общая ошибка\n\n', ex)

            await CheckProfiles.waiting.set()

            print(all_matches)

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

        if DataBaseWork().get_data_from_profiles_table('is_matched', callback.from_user.id) == True:
            DataBaseWork().update_viewed_ids(all_matches.split()[-1], callback.from_user.id)
            DataBaseWork().add_user_in_violators_table(all_matches.split()[-1])

            try:
                index = all_matches.find(f'{all_matches.split()[-1]}')
                all_matches = all_matches[:index - 1]
            except:
                all_matches = -1

            DataBaseWork().set_data_in_table('match_id', all_matches, callback.from_user.id, 'users')

        else:
            DataBaseWork().update_viewed_ids(DataBaseWork().get_data_from_profiles_table('now_check_id', callback.from_user.id), callback.from_user.id)
            DataBaseWork().add_user_in_violators_table(DataBaseWork().get_data_from_profiles_table('now_check_id', callback.from_user.id))

        await callback.message.answer('Жалоба отправлена!')
        await CheckProfiles.check.set()
        await start_check_profiles(callback)

async def is_view_match_profile(callback: types.CallbackQuery):
    if DataBaseWork().is_user_blocked(callback.from_user.id) == False:
        await is_change_user_name(callback)

        print('Я ЕЩЕ НЕ СЛОМАЛСЯ')
        list_osther_id = (DataBaseWork().get_data_from_profiles_table('mutual_id', callback.from_user.id)).split()

        if list_osther_id[0] != '-1':
            print(list_osther_id)
            other_id = int(list_osther_id[-1])
            print(other_id)

            photo_or_video_id = DataBaseWork().get_data_from_profiles_table('photo_or_video_id', other_id)

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
        else:
            await callback.message.answer('Анкеты людей, с которыми у тебя случился мэтч, закончились!')

        if DataBaseWork().is_exist_user_in_db(callback.from_user.id, 'admins') == True:
            await callback.message.answer('Чтобы продолжить знакомство с людьми, нажми 🫰🏼Найти друга', reply_markup=buttons.menu_admin)
        else:
            await callback.message.answer('Чтобы продолжить знакомство с людьми, нажми 🫰🏼Найти друга', reply_markup=buttons.menu)

async def correctness_profile_text(profile_text):
    if len(profile_text) > 990:
        profile_text = profile_text[0:990]
        profile_text += ' ...'

    return profile_text

async def is_menu(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text in ['🫰🏼Найти друга', '👤 Мой профиль', 'Выбор режима','⛔ Скрыть анкету', '⛑ Проблема с ботом']:
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