import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import db
from handlers import viewing_questionnaires, menu, admin

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
    await msg.answer('Пожалуйста, напиши свое имя (просто имя, без фамилии и отчества) 👇')
    await MyProfileStates.name.set()

async def insert_name_handler(message: types.Message):
    db.set_data_in_table('user_name', message.text, message.from_user.id, 'users')
    await MyProfileStates.age.set()
    await message.answer('Сколько тебе лет?')

'''insert_age'''
async def insert_age_handler(message: types.Message):
    if message.text.isdigit() == True and int(message.text) > 9 and int(message.text) < 100:
        db.set_data_in_table('age', message.text, message.from_user.id, 'users')
        await MyProfileStates.sex.set()
        await message.answer('Теперь определимся с полом:', reply_markup=buttons.sex)
    else:
        await message.answer('Укажи правильный возраст, только цифры')

'''insert_sex'''
async def insert_sex_handler(message: types.Message):
    if message.text not in ['Я девушка', 'Я парень']:
        await message.answer('Нет такого варианта ответа', reply_markup=buttons.sex)
    else:
        db.set_data_in_table('gender', message.text, message.from_user.id, 'users')
        await MyProfileStates.who_do_you_like.set()
        await message.answer('Кто тебе интересен?', reply_markup=buttons.who_do_you_like)

'''insert_who_do_you_like'''
async def insert_who_do_you_like_handler(message: types.Message):
    if message.text not in ['Девушки', 'Парни', 'Все равно']:
        await message.answer('Нет такого варианта ответа', reply_markup=buttons.who_do_you_like)
    else:
        db.set_data_in_table('opposite', message.text, message.from_user.id, 'users')
        await MyProfileStates.city.set()
        await message.answer('Напиши твой город. Без указания страны и региона 👇', reply_markup=buttons.remove_markup)
###

'''insert_city'''
async def insert_city_handler(message: types.Message):
    db.set_data_in_table('city', message.text, message.from_user.id, 'users')
    await MyProfileStates.dop_info.set()

    # 'AgACAgIAAxkBAAISlmPCrb4tAl1hfx2XCTEz-yTuS90VAALnxTEb9pkYShUo-Em7Ubu7AQADAgADcwADLQQ' # фото для @Bratek_bot
    # 'AgACAgIAAxkBAAMaY8QLVOsHLiCJbM_a3yxb3j7kqdIAAm7EMRszmCBKuo1NGBdPK3wBAAMCAANzAAMtBA'  # фото для @ktinder_bot
    await bot.send_photo(message.from_user.id, photo='AgACAgIAAxkBAAMaY8QLVOsHLiCJbM_a3yxb3j7kqdIAAm7EMRszmCBKuo1NGBdPK3wBAAMCAANzAAMtBA',
                   caption='Выпиши словами из списка (на фото) 3 пункта, '
                           'либо предложи свой вариант. Почему ты выбрал именно эти 3 пункта?\n'
                           'Формат записи:\n'
                           '*первый вариант*\n'
                           '*второй вариант*\n'
                           '*третий вариант*\n'
                           '*Я выбрал эти варианты потому что...*')
###

'''dop_info'''
async def insert_dop_info_handler(message: types.Message):
    db.set_data_in_table('dop_info', message.text, message.from_user.id, 'users')
    await dop_info_module(message)

async def dop_info_module(msg):
    await MyProfileStates.description_of_yourself.set()

    await msg.answer('Коротко расскажи о себе и кого хочешь найти, чем предлагаешь заняться.'
                         ' Это поможет лучше подобрать тебе компанию.')
###


'''insert_description_of_yourself'''
async def insert_description_of_yourself_handler(message: types.Message):
    await insert_description_of_yourself_module(message, False)

async def insert_description_of_yourself_module(msg, flag):
    if flag == False:
        if msg.text == 'Пропустить':
            db.set_data_in_table('description', '', msg.from_user.id, 'users')
        else:
            db.set_data_in_table('description', msg.text, msg.from_user.id, 'users')

        if db.get_data_from_profiles_table('changes', msg.from_user.id) == 3:
            await output_from_profile(msg)
            return

    if db.get_data_from_profiles_table('changes', msg.from_user.id) == 3:
        await MyProfileStates.photo_or_video.set()
        await insert_photo_or_video_module(msg, True)
    else:
        await MyProfileStates.photo_or_video.set()
        await msg.answer('Теперь пришли фото или запиши видео 👍 (до 15 сек), его будут '
                         'видеть другие пользователи', reply_markup=buttons.remove_markup)
###


'''insert_photo_or_video'''
async def insert_photo_or_video_handler(message: types.Message):
    if message.photo or message.video:
        await insert_photo_or_video_module(message, False)
    else:
        await message.answer('Пришли фото или видео (до 15 сек)')


async def insert_photo_or_video_module(msg, flag):
    if flag == False:
        if msg.photo:
            db.set_data_in_table('photo_or_video_id', msg.photo[0].file_id, msg.from_user.id, 'users')
        elif msg.video:
            db.set_data_in_table('photo_or_video_id', msg.video.file_id, msg.from_user.id, 'users')

    await output_from_profile(msg)
###

'''yes_or_no'''
async def yes_or_no_handler(message: types.Message):
    if message.text == 'Да':
        db.set_data_in_table('changes', 0, message.from_user.id, 'users')
        await message.answer('Супер!\n\n'
                             'Тыкай на кнопку «💌 Тиндер» в меню, смотри видео-фото профили участников и ставь 👍 и 👎. '
                             'Когда реакция будет взаимна, то бот отправит уведомление и контакты участника.\n\n',
                             reply_markup=buttons.menu)
        await menu.MenuState.menu.set()

    elif message.text == 'Изменить анкету':
        await message.answer('1. Заполнить анкету заново.\n'
                             '2. Изменить фото/видео.\n'
                             '3. Изменить текст анкеты.\n'
                             '4. Все верно.\n', reply_markup=buttons.numbers)

        await MyProfileStates.profile_changes.set()
    else:
        await message.answer('Нет такого варианта ответа')
###

'''profile_changes'''
async def profile_changes_handler(message: types.Message):
    if message.text == '1':
        db.set_data_in_table('changes', 1, message.from_user.id, 'users')
        await start_myprofile_module(message)

    elif message.text == '2':
        db.set_data_in_table('changes', 2, message.from_user.id, 'users')
        await insert_description_of_yourself_module(message, True)

    elif message.text == '3':
        db.set_data_in_table('changes', 3, message.from_user.id, 'users')
        await dop_info_module(message)

    elif message.text == '4 🚀':
        db.set_data_in_table('changes', 0, message.from_user.id, 'users')
        await menu.MenuState.menu.set()
        await message.answer('Супер, ты заполнил профиль! '
                             'Теперь ты можешь видеть других участников.\n\n'
                             'Cмотри видео-фото профили участников и ставь 👍 и 👎. '
                             'Когда реакция будет взаимна, то бот отправит уведомление и контакты участника.\n\n'
                             'Погнали!',
                             reply_markup=buttons.menu)
###

async def output_from_profile(msg):
    await msg.answer('Так выглядит твоя анкета:')

    photo_or_video_id = db.get_data_from_profiles_table('photo_or_video_id', msg.from_user.id)

    if db.get_data_from_profiles_table('description', msg.from_user.id) == '':
        str = f"{db.get_data_from_profiles_table('user_name', msg.from_user.id)}, " \
              f"{db.get_data_from_profiles_table('age', msg.from_user.id)}, " \
              f"{db.get_data_from_profiles_table('city', msg.from_user.id)}." \
              f"{db.get_data_from_profiles_table('dop_info', msg.from_user.id)}"

    else:
        str = f"{db.get_data_from_profiles_table('user_name', msg.from_user.id)}, " \
              f"{db.get_data_from_profiles_table('age', msg.from_user.id)}, " \
              f"{db.get_data_from_profiles_table('city', msg.from_user.id)} - " \
              f"{db.get_data_from_profiles_table('description', msg.from_user.id)}.\n" \
              f"{db.get_data_from_profiles_table('dop_info', msg.from_user.id)}"

    try:
        await bot.send_photo(chat_id=msg.from_user.id, photo=photo_or_video_id, caption=str)
    except:
        await bot.send_video(chat_id=msg.from_user.id, video=photo_or_video_id, caption=str)

    await MyProfileStates.confirmation.set()

    await msg.answer('Все верно?', reply_markup=buttons.yes_or_no)

async def is_menu(message: types.Message):
    if message.text in ['💌 Тиндер', '👤 Мой профиль', '🙋‍♀ Поддержка️']:
        await menu.menu_module(message)

# async def is_admin(msg):
#     if msg.text == '/admin':
#         await admin.AdminStates.admin_menu.set()
#         await admin.admin_menu_handler(msg)

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


