import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import DataBaseWork
from handlers import viewing_questionnaires, menu, admin
import re
import start_bot

async def is_change_user_name(msg):
    return DataBaseWork().set_data_in_table('user_nickname', msg.from_user.username, msg.from_user.id, 'users')

class MyProfileStates(StatesGroup):
    name = State()
    age = State()
    sex = State()
    who_do_you_like = State()
    city = State()
    dop_info = State()
    description_of_yourself = State()
    photo_or_video = State()
    confirmation = State()
    profile_changes = State()

'''start_myprofile'''
async def start_myprofile_handler(message: types.Message):
    await start_myprofile_module(message)

async def start_myprofile_module(msg):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        await is_change_user_name(msg)

        await MyProfileStates.name.set()
        await msg.answer('Пожалуйста, напиши свое имя (просто имя, без фамилии и отчества) 👇')

async def insert_name_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)
        if DataBaseWork().get_data_from_profiles_table('changes', message.from_user.id) == 2:
            await message.answer('Сколько тебе лет?')
            await MyProfileStates.age.set()

        else:
            DataBaseWork().set_data_in_table('user_name', message.text, message.from_user.id, 'users')
            await MyProfileStates.age.set()
            await message.answer('Сколько тебе лет?')


'''insert_age'''
async def insert_age_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)
        print(type(DataBaseWork().get_data_from_profiles_table('changes', message.from_user.id)),' : ' , DataBaseWork().get_data_from_profiles_table('changes', message.from_user.id))
        if DataBaseWork().get_data_from_profiles_table('changes', message.from_user.id) == 2:
            if message.text.isdigit() == True and int(message.text) > 9 and int(message.text) < 100:
                DataBaseWork().set_data_in_table('age', message.text, message.from_user.id, 'users')
                return await output_from_profile(message)
            else:
                await message.answer('Укажи правильный возраст, только цифры')
        else:
            if message.text.isdigit() == True and int(message.text) > 9 and int(message.text) < 100:
                DataBaseWork().set_data_in_table('age', message.text, message.from_user.id, 'users')
                await MyProfileStates.sex.set()
                await message.answer('Теперь определимся с полом:', reply_markup=buttons.sex)
            else:
                await message.answer('Укажи правильный возраст, только цифры')

'''insert_sex'''
async def insert_sex_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)

        elif message.text not in ['Я девушка', 'Я парень']:
            await message.answer('Нет такого варианта ответа', reply_markup=buttons.sex)
        else:
            DataBaseWork().set_data_in_table('gender', message.text, message.from_user.id, 'users')
            await MyProfileStates.who_do_you_like.set()
            await message.answer('Кто тебе интересен?', reply_markup=buttons.who_do_you_like)

'''insert_who_do_you_like'''
async def insert_who_do_you_like_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)

        if DataBaseWork().get_data_from_profiles_table('changes', message.from_user.id) == 3:
            await MyProfileStates.city.set()
            await message.answer('Напиши твой город. Без указания страны, региона, цифр и нарусском языке👇',
                                 reply_markup=buttons.remove_markup)
        else:
            if message.text not in ['Девушки', 'Парни', 'Все равно']:
                await message.answer('Нет такого варианта ответа', reply_markup=buttons.who_do_you_like)
            else:
                DataBaseWork().set_data_in_table('opposite', message.text, message.from_user.id, 'users')
                await MyProfileStates.city.set()
                await message.answer('Напиши твой город. Без указания страны, региона, цифр и на русском языке👇',
                                     reply_markup=buttons.remove_markup)
###

async def is_russian(s: str) -> bool:
    return bool(re.fullmatch(r'(?i)[а-яё -]+', s))

'''insert_city'''
async def insert_city_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)

        if DataBaseWork().get_data_from_profiles_table('changes', message.from_user.id) == 3:
            if await is_russian(message.text) == True:
                DataBaseWork().set_data_in_table('city', message.text, message.from_user.id, 'users')
                return await output_from_profile(message)
            else:
                await message.answer('Напиши твой город. Без указания страны, региона, цифр и на русском языке👇', reply_markup=buttons.remove_markup)
        else:
            if await is_russian(message.text) == True:
                DataBaseWork().set_data_in_table('city', message.text, message.from_user.id, 'users')
                await MyProfileStates.dop_info.set()
                
                await message.answer('Расскажи о своих увлечениях и интересах. Напиши 3 вещи, которые тебе нравятся.\n\n'
                                   'Например:\n\n'
                                   'Путешествия\n'
                                   'Кулинария\n'
                                   'Фильмы\n\n'
                                   'Люблю путешествовать, открывать для себя новые места. '
                                   'Увлекаюсь приготовлением разных блюд. '
                                   'В свободное время смотрю интересные фильмы.')
            else:
                await message.answer('Напиши твой город. Без указания страны, региона, цифр и на русском языке👇',
                                     reply_markup=buttons.remove_markup)
        ###
###

'''dop_info'''
async def insert_dop_info_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)

        DataBaseWork().set_data_in_table('dop_info', message.text, message.from_user.id, 'users')

        if DataBaseWork().get_data_from_profiles_table('changes', message.from_user.id) == 6:
            await output_from_profile(message)
        else:
            await dop_info_module(message)

async def dop_info_module(msg):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        await is_change_user_name(msg)

        if msg.text == '/start':
            return await start_bot.command_start_module(msg)

        await MyProfileStates.description_of_yourself.set()

        await msg.answer('Коротко расскажи о себе и кого хочешь найти, чем предлагаешь заняться.'
                             ' Это поможет лучше подобрать тебе компанию.')
###


'''insert_description_of_yourself'''
async def insert_description_of_yourself_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)
        await insert_description_of_yourself_module(message, False)


async def insert_description_of_yourself_module(msg, flag):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        await is_change_user_name(msg)

        if msg.text == '/start':
            return await start_bot.command_start_module(msg)
        if flag == False:
            if msg.text == 'Пропустить':
                DataBaseWork().set_data_in_table('description', '', msg.from_user.id, 'users')
            else:
                DataBaseWork().set_data_in_table('description', msg.text, msg.from_user.id, 'users')

            if DataBaseWork().get_data_from_profiles_table('changes', msg.from_user.id) == 5:
                return await output_from_profile(msg)

        await MyProfileStates.photo_or_video.set()
        await msg.answer('Теперь пришли фото или запиши видео 👍 (до 15 сек), его будут '
                         'видеть другие пользователи', reply_markup=buttons.remove_markup)
###


'''insert_photo_or_video'''
async def insert_photo_or_video_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)

        if message.photo or message.video:
            await insert_photo_or_video_module(message, False)
        else:
            await message.answer('Пришли фото или видео (до 15 сек)')


async def insert_photo_or_video_module(msg, flag):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        await is_change_user_name(msg)

        if msg.text == '/start':
            return await start_bot.command_start_module(msg)
        if flag == False:
            if msg.photo:
                DataBaseWork().set_data_in_table('photo_or_video_id', msg.photo[0].file_id, msg.from_user.id, 'users')
            elif msg.video:
                DataBaseWork().set_data_in_table('photo_or_video_id', msg.video.file_id, msg.from_user.id, 'users')

        await output_from_profile(msg)
###

'''yes_or_no'''
async def yes_or_no_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)

        elif message.text == 'Да':
            DataBaseWork().set_data_in_table('changes', 0, message.from_user.id, 'users')
            await menu.MenuState.menu.set()
            if DataBaseWork().is_exist_user_in_db(message.from_user.id, 'admins') == True:
                await message.answer('Супер, ты заполнил профиль! '
                                     'Теперь ты можешь видеть других участников.\n\n'
                                     'Cмотри видео-фото профили участников и ставь 👍 и 👎. '
                                     'Когда реакция будет взаимна, то бот отправит уведомление и контакты участника.\n\n'
                                     'Погнали!',
                                     reply_markup=buttons.menu_admin)
            else:
                await message.answer('Супер, ты заполнил профиль! '
                                     'Теперь ты можешь видеть других участников.\n\n'
                                     'Cмотри видео-фото профили участников и ставь 👍 и 👎. '
                                     'Когда реакция будет взаимна, то бот отправит уведомление и контакты участника.\n\n'
                                     'Погнали!',
                                     reply_markup=buttons.menu)

        elif message.text == 'Изменить анкету':
            await message.answer('1. Заполнить анкету заново.\n'
                                 '2. Изменить возраст.\n'
                                 '3. Изменить город.\n'
                                 '4. Изменить фото/видео.\n'
                                 '5. Изменить текст анкеты.\n'
                                 '6. Изменить выбор слов из списка.\n'
                                 '7 🚀. Все верно.\n', reply_markup=buttons.numbers)

            await MyProfileStates.profile_changes.set()
        else:
            await message.answer('Нет такого варианта ответа')
###

'''profile_changes'''
async def profile_changes_handler(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text == '/start':
            return await start_bot.command_start_module(message)

        elif message.text == '1':
            DataBaseWork().set_data_in_table('changes', 1, message.from_user.id, 'users')
            DataBaseWork().set_data_in_table('viewed_ids', 'None', message.from_user.id, 'users')
            await start_myprofile_module(message)

        elif message.text == '2':
            DataBaseWork().set_data_in_table('changes', 2, message.from_user.id, 'users')
            DataBaseWork().set_data_in_table('age', -1, message.from_user.id, 'users')
            await insert_name_handler(message)

        elif message.text == '3':
            DataBaseWork().set_data_in_table('changes', 3, message.from_user.id, 'users')
            await insert_who_do_you_like_handler(message)

        elif message.text == '4':
            DataBaseWork().set_data_in_table('changes', 4, message.from_user.id, 'users')
            await insert_description_of_yourself_module(message, True)

        elif message.text == '5':
            DataBaseWork().set_data_in_table('changes', 5, message.from_user.id, 'users')
            await dop_info_module(message)

        elif message.text == '6':
            DataBaseWork().set_data_in_table('changes', 6, message.from_user.id, 'users')
            await MyProfileStates.dop_info.set()
            await message.answer('Расскажи о своих увлечениях и интересах. Напиши 3 вещи, которые тебе нравятся.\n\n'
                               'Например:\n\n'
                               'Путешествия\n'
                               'Кулинария\n'
                               'Фильмы\n\n'
                               'Люблю путешествовать, открывать для себя новые места. '
                               'Увлекаюсь приготовлением разных блюд. '
                               'В свободное время смотрю интересные фильмы.')

        elif message.text == '7 🚀':
            DataBaseWork().set_data_in_table('changes', 0, message.from_user.id, 'users')
            await menu.MenuState.menu.set()
            if DataBaseWork().is_exist_user_in_db(message.from_user.id, 'admins') == True:
                await message.answer('Супер, ты заполнил профиль! '
                                     'Теперь ты можешь видеть других участников.\n\n'
                                     'Cмотри профили участников и ставь 👍 и 👎. '
                                     'Когда реакция будет взаимна, то бот отправит уведомление и контакты участника.\n\n'
                                     'Погнали!',
                                     reply_markup=buttons.menu_admin)
            else:
                await message.answer('Супер, ты заполнил профиль! '
                                     'Теперь ты можешь видеть других участников.\n\n'
                                     'Cмотри профили участников и ставь 👍 и 👎. '
                                     'Когда реакция будет взаимна, то бот отправит уведомление и контакты участника.\n\n'
                                     'Погнали!',
                                     reply_markup=buttons.menu)
###

async def output_from_profile(msg):
    if DataBaseWork().is_user_blocked(msg.from_user.id) == False:
        await msg.answer('Так выглядит твоя анкета:')

        photo_or_video_id = DataBaseWork().get_data_from_profiles_table('photo_or_video_id', msg.from_user.id)

        if photo_or_video_id != '':

            if DataBaseWork().get_data_from_profiles_table('description', msg.from_user.id) == '':
                str = f"{DataBaseWork().get_data_from_profiles_table('user_name', msg.from_user.id)}, " \
                      f"{DataBaseWork().get_data_from_profiles_table('age', msg.from_user.id)}, " \
                      f"{DataBaseWork().get_data_from_profiles_table('city', msg.from_user.id)}.\n\n" \
                      f"{DataBaseWork().get_data_from_profiles_table('dop_info', msg.from_user.id)}"

            else:
                str = f"{DataBaseWork().get_data_from_profiles_table('user_name', msg.from_user.id)}, " \
                      f"{DataBaseWork().get_data_from_profiles_table('age', msg.from_user.id)}, " \
                      f"{DataBaseWork().get_data_from_profiles_table('city', msg.from_user.id)} - " \
                      f"{DataBaseWork().get_data_from_profiles_table('description', msg.from_user.id)}.\n\n" \
                      f"{DataBaseWork().get_data_from_profiles_table('dop_info', msg.from_user.id)}"

            if len(str) >= 1012 - len(DataBaseWork().get_data_from_profiles_table('user_nickname', msg.from_user.id)):
                await bot.send_message(msg.from_user.id, f'Описание вашей анкеты превышает допустимый лимит символов\.\n'
                                                         f'***{len(str)}/1024***\n'
                                                         f'Пройдите регистрацию повторно', parse_mode=types.ParseMode.MARKDOWN_V2)
                return await start_myprofile_module(msg)

            try:
                await bot.send_photo(chat_id=msg.from_user.id, photo=photo_or_video_id, caption=str)
            except:
                await bot.send_video(chat_id=msg.from_user.id, video=photo_or_video_id, caption=str)

            await MyProfileStates.confirmation.set()

            await msg.answer('Все верно?', reply_markup=buttons.yes_or_no)
        else:
            await MyProfileStates.confirmation.set()

            await msg.answer('Все верно?', reply_markup=buttons.yes_or_no)

async def is_menu(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        await is_change_user_name(message)

        if message.text in ['Найти друга', '👤 Мой профиль', 'Выбор режима','⛔ Скрыть анкету', '⛑ Проблема с ботом']:
            await menu.menu_module(message)
        elif message.text == '/start':
            await start_bot.command_start_module(message)

def reg_handlers_questionnaire(dp : Dispatcher):
    dp.register_message_handler(start_myprofile_handler, commands='myprofile', state=None)
    dp.register_message_handler(insert_name_handler, state=MyProfileStates.name)
    dp.register_message_handler(insert_age_handler, state=MyProfileStates.age)
    dp.register_message_handler(insert_sex_handler, state=MyProfileStates.sex)
    dp.register_message_handler(insert_who_do_you_like_handler, state=MyProfileStates.who_do_you_like)
    dp.register_message_handler(insert_city_handler, state=MyProfileStates.city)
    dp.register_message_handler(insert_dop_info_handler, state=MyProfileStates.dop_info)
    dp.register_message_handler(insert_description_of_yourself_handler, state=MyProfileStates.description_of_yourself)
    dp.register_message_handler(insert_photo_or_video_handler, content_types=types.ContentType.ANY, state=MyProfileStates.photo_or_video)
    dp.register_message_handler(yes_or_no_handler, state=MyProfileStates.confirmation)
    dp.register_message_handler(profile_changes_handler, state=MyProfileStates.profile_changes)
    dp.register_message_handler(is_menu, state=menu.MenuState.menu)
