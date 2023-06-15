import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import DataBaseWork
from aiogram.dispatcher.filters import Text
from handlers import viewing_questionnaires, menu, change_mode
import os
import start_bot

class AdminStates(StatesGroup):
    admin_menu = State()

    first_choice = State()

    user_to_admin = State()
    admin_to_user = State()

    mailing_choice = State()
    choise_sex = State()
    get_mail = State()
    save_mail = State()
    send_out_mail = State()

    settings = State()
    settings_choice = State()
    settings_warn = State()
    settings_block = State()
    settings_unblock = State()

    analytics = State()

'''*** Главное меню администратора ***'''
'''******************************************************************************************************************'''
async def admin_menu_handler(message: types.Message):
    await admin_menu_module(message)

async def admin_menu_module(msg):
    await AdminStates.first_choice.set()
    await msg.answer('Выберите действие:', reply_markup=buttons.start_admin_menu)

async def first_chocie_handler(message: types.Message):
    if message.text == '📣 Сделать рассылку пользователям':
        await AdminStates.mailing_choice.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)
    elif message.text == '⚙ Настройки':
        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)
    elif message.text == '🗂 Аналитика':
        await AdminStates.analytics.set()
        await analytics(message)
    elif message.text == '🔙 Вернуться к выбору режима':
        await change_mode.change_mode_module(message)
    elif message.text == 'Повысить до администратора':
        await AdminStates.user_to_admin.set()
        await message.answer('Введите id обычного пользователя, которого хотите сделать администратором:',
                             reply_markup=buttons.cancel_reply)
    elif message.text == 'Понизить до обычного пользователя':
        await AdminStates.admin_to_user.set()
        await message.answer('Введите id администратора, которого хотите сделать обычным пользователем:',
                             reply_markup=buttons.cancel_reply)
    else:
        await message.answer('Нет такого варианта!')
'''******************************************************************************************************************'''

'''*** Повышение до администратора ***'''
'''******************************************************************************************************************'''
async def from_user_to_admin(message: types.Message):
    if message.text == 'Отмена':
        await admin_menu_module(message)
    else:
        try:
            DataBaseWork().add_user_in_admins_table(int(message.text))
            await message.answer('Пользователь успепшно повышен до звания <b>"Администратор"</b>!',
                                 parse_mode='HTML')
            await admin_menu_module(message)
        except:
            await message.answer('Произошла ошибка при повышении пользователя до звания <b>"Администратор"</b>! '
                                 'Возможно id пользователя, который вы прислали - некорректный '
                                 'или пользователь уже является Администратором!\n\n'
                                 'Введите id повторно или нажмите кнопку <b>Отмена</b>',
                                 parse_mode='HTML',
                                 reply_markup=buttons.cancel_reply)
'''******************************************************************************************************************'''

'''*** Понижение до обычного пользователя ***'''
'''******************************************************************************************************************'''
async def from_admin_to_user(message: types.Message):
    if message.text == 'Отмена':
        await admin_menu_module(message)
    else:
        try:
            DataBaseWork().delete_user_from_admins_table(int(message.text))
            await message.answer('Администратор успепшно понижен до звания <b>"Обычный пользователь"</b>!',
                                 parse_mode='HTML')
            await admin_menu_module(message)
        except:
            await message.answer('Произошла ошибка при понижении Администратора до звания <b>"Обычный пользователь"</b>! '
                                 'Возможно id Администратора, который вы прислали - некорректный '
                                 'или Администратор уже был понижен!\n\n'
                                 'Введите id повторно или нажмите кнопку <b>Отмена</b>',
                                 parse_mode='HTML',
                                 reply_markup=buttons.cancel_reply)
'''******************************************************************************************************************'''


'''*** Меню выбор типа рассылки ***'''
'''******************************************************************************************************************'''
async def mailing_choice(message: types.Message):
    if message.text == '🔔 Обычная рассылка':
        DataBaseWork().set_data_in_table('mailing_to', 'Всем', message.from_user.id, 'admins')
        await AdminStates.get_mail.set()
        await message.answer('Присылайте текст, фотографии и видео (и/или с текстом) для будущей рассылки '
                             'и нажмите <b>Сохранить</b>, когда будете готовы.\n\n'
                             '⚠️ Присылая сообщения, дождитесь ответа бота о его успешном добавлении к рассылке.',
                             reply_markup=buttons.cancel_reply,
                             parse_mode='HTML')
    elif message.text == '👥 Конкретным пользователям':
        await AdminStates.choise_sex.set()
        await message.answer('Выберите кому надо разослать:', reply_markup=buttons.mailing_specific)
    elif message.text == '🔙 Вернуться в меню':
        await admin_menu_module(message)
    else:
        await message.answer('Нет такого варианта!', reply_markup=buttons.mailing_admin_menu)

# Выбор получателей
async def choise_sex_for_mailing_to_specific(message: types.Message):
    if message.text == 'Девушкам':
        DataBaseWork().set_data_in_table('mailing_to', 'Девушкам', message.from_user.id, 'admins')
        await AdminStates.get_mail.set()
        await message.answer('Присылайте текст, фотографии и видео (и/или с текстом) для будущей рассылки '
                             'и нажмите <b>Сохранить</b>, когда будете готовы.\n\n'
                             '⚠️ Присылая сообщения, дождитесь ответа бота о его успешном добавлении к рассылке.',
                             reply_markup=buttons.cancel_reply,
                             parse_mode='HTML')
    elif message.text == 'Парням':
        DataBaseWork().set_data_in_table('mailing_to', 'Парням', message.from_user.id, 'admins')
        await AdminStates.get_mail.set()
        await message.answer('Присылайте текст, фотографии и видео (и/или с текстом) для будущей рассылки '
                             'и нажмите <b>Сохранить</b>, когда будете готовы.\n\n'
                             '⚠️ Присылая сообщения, дождитесь ответа бота о его успешном добавлении к рассылке.',
                             reply_markup=buttons.cancel_reply,
                             parse_mode='HTML')
    elif message.text == 'Отмена':
        await delete_mail(message)

        await AdminStates.mailing_choice.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)
    else:
        await message.answer('Нет такого варианта!')

# Получение поста от админа
async def get_mail_from_admin(message: types.Message):
    if message.text == 'Отмена':
        await delete_mail(message)

        await AdminStates.mailing_choice.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)
    else:
        if message.photo:
            DataBaseWork().add_photo_or_video_to_admins(message.from_user.id, message.photo[0].file_id)
            DataBaseWork().set_data_in_table('mail_text', message.caption, message.from_user.id, 'admins')
        elif message.video:
            DataBaseWork().add_photo_or_video_to_admins(message.from_user.id, message.video.file_id)
            DataBaseWork().set_data_in_table('mail_text', message.caption, message.from_user.id, 'admins')
        elif message.text:
            DataBaseWork().set_data_in_table('mail_text', message.text, message.from_user.id, 'admins')

        await AdminStates.save_mail.set()
        await message.answer('Сообщение успешно добавлено к рассылке. Нажмите <b>Сохранить</b>, '
                             'чтобы завершить ее формирование.', parse_mode='HTML', reply_markup=buttons.save_or_no)

# Сохранение поста
async def save_mail(message: types.Message):
    if message.text == 'Сохранить':
        await AdminStates.send_out_mail.set()
        await message.answer('Рассылка создана. Отправляем?', reply_markup=buttons.yes_or_no_send_mail)
    elif message.text == 'Отмена':
        await delete_mail(message)

        await AdminStates.mailing_choice.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)
    else:
        await message.answer('Нет такого варианта!')

# Рассылка
# работает долго
async def send_out_mail(message: types.Message):
    if message.text == '✅ Да':
        all_id = 0

        if DataBaseWork().get_data_from_admins_table('mailing_to', message.from_user.id) == 'Всем':
            all_id = DataBaseWork().get_all_users_id()
        elif DataBaseWork().get_data_from_admins_table('mailing_to', message.from_user.id) == 'Девушкам':
            all_id = DataBaseWork().get_all_specific_users_id('Девушкам')
        elif DataBaseWork().get_data_from_admins_table('mailing_to', message.from_user.id) == 'Парням':
            all_id = DataBaseWork().get_all_specific_users_id('Парням')


        users_counter = 0
        for i in range(len(all_id)):
            try:
                await bot.send_photo(chat_id=int(all_id[i]),
                                     photo=DataBaseWork().get_data_from_admins_table('photo_video_ids', message.from_user.id),
                                     caption=DataBaseWork().get_data_from_admins_table('mail_text', message.from_user.id))
                users_counter += 1
            except:
                try:
                    await bot.send_video(chat_id=int(all_id[i]),
                                         video=DataBaseWork().get_data_from_admins_table('photo_video_ids', message.from_user.id),
                                         caption=DataBaseWork().get_data_from_admins_table('mail_text', message.from_user.id))
                    users_counter += 1
                except:
                    try:
                        await bot.send_message(chat_id=int(all_id[i]),
                                               text=DataBaseWork().get_data_from_admins_table('mail_text', message.from_user.id))
                        users_counter += 1
                    except:
                        pass

        await message.answer(f'✅ Рассылка успешно завершена для <b>{users_counter}/{len(all_id)} человек</b>', parse_mode='HTML')
        await AdminStates.mailing_choice.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)

    elif message.text == '❎ Нет':
        await AdminStates.mailing_choice.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)

    await delete_mail(message)

async def delete_mail(msg):
    DataBaseWork().set_data_in_table('mailing_to', None, msg.from_user.id, 'admins')
    DataBaseWork().set_data_in_table('photo_video_ids', None, msg.from_user.id, 'admins')
    DataBaseWork().set_data_in_table('mail_text', None, msg.from_user.id, 'admins')

'''******************************************************************************************************************'''

'''*** Меню выбора типа настройки ***'''
'''******************************************************************************************************************'''
async def settings_handler(message: types.Message):
    await settings_module(message, 0)

async def settings_module(msg, flag):
    if msg.text in ['Предупредить', 'Заблокировать', 'Разблокировать пользователя']:
        DataBaseWork().set_data_in_table('viewed_ids', '-1', msg.from_user.id, 'admins')

    if msg.text == 'Предупредить' or flag == 1:
        try:
            violator_id = DataBaseWork().find_violator(msg.from_user.id, 'void')
            await output_from_profile(msg.from_user.id, violator_id)

            await AdminStates.settings_warn.set()
            await msg.answer(f'На эту анкету поступило '
                                 f'{DataBaseWork().get_data_from_violators_table(DataBaseWork().get_data_from_admins_table("violators_id", msg.from_user.id), "number_of_complaints")}'
                                 f' жалоб(-а/-ы)!\n'
                                 'Выберите действие:', reply_markup=buttons.settings_warn)
        except:
            await AdminStates.settings.set()
            await msg.answer('Нарушители не найдены!')
            await msg.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif msg.text == 'Заблокировать' or flag == 2:
        try:
            violator_id = DataBaseWork().find_violator(msg.from_user.id, 'Предупрежден')
            await output_from_profile(msg.from_user.id, violator_id)

            await AdminStates.settings_block.set()
            await msg.answer(f'На эту анкету поступило '
                                 f'{DataBaseWork().get_data_from_violators_table(DataBaseWork().get_data_from_admins_table("violators_id", msg.from_user.id), "number_of_complaints")}'
                                 f' жалоб(-а)!\n'
                                 'Выберите действие:', reply_markup=buttons.settings_block)
        except:
            await AdminStates.settings.set()
            await msg.answer('Предупрежденные пользователи не найдены!')
            await msg.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif msg.text == 'Разблокировать пользователя' or flag == 3:
        try:
            violator_id = DataBaseWork().find_violator(msg.from_user.id, 'Заблокирован')
            await output_from_profile(msg.from_user.id, violator_id)

            await AdminStates.settings_unblock.set()
            await msg.answer(f'На эту анкету поступило '
                                 f'{DataBaseWork().get_data_from_violators_table(DataBaseWork().get_data_from_admins_table("violators_id", msg.from_user.id), "number_of_complaints")}'
                                 f' жалоб(-а)!\n'
                                 'Выберите действие:', reply_markup=buttons.settings_unblock)
        except:
            await AdminStates.settings.set()
            await msg.answer('Заблокированные пользователи не найдены!')
            await msg.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif msg.text == '🔙 Вернуться в меню':
        await admin_menu_module(msg)
    else:
        await msg.answer('Нет такого варианта!')

async def warn(message: types.Message):
    if message.text == 'Предупредить':
        try:
            await bot.send_message(DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id),
                               'Вам пришло предупреждение от Администратора!\n'
                               'Следующее предупреждение - бан!')
        except:
            pass

        DataBaseWork().set_data_in_table(
            'status', 'Предупрежден', DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id),
            'violators')

        DataBaseWork().set_data_in_table(
            'number_of_complaints', 0, DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id),
            'violators')

        DataBaseWork().set_data_in_table('inactive', -1, DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id), 'users')

        await AdminStates.settings.set()
        await message.answer('Предупреждение отправлено!')
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif message.text == 'Помиловать':
        DataBaseWork().delete_user_from_violators_table(DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id))
        await message.answer('Пользователь помилован!')

        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif message.text == 'Далее':
        await settings_module(message, 1)

    elif message.text == 'Отмена':
        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)
    else:
        await message.answer('Нет такого варианта!')

async def block(message: types.Message):
    if message.text == 'Заблокировать':
        try:
            await bot.send_message(DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id),
                                   'Вы были забанены Администратором!')
        except:
            pass
        DataBaseWork().set_data_in_table('inactive',
                                         -1,
                                         DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id),
                                         'users')
        DataBaseWork().set_data_in_table(
            'status', 'Заблокирован', DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id),
            'violators')

        DataBaseWork().set_data_in_table('number_of_complaints', 0, message.from_user.id, 'violators')

        await AdminStates.settings.set()
        await message.answer('Пользователь заблокирован!')
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif message.text == 'Помиловать':
        DataBaseWork().delete_user_from_violators_table(DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id))
        await message.answer('Пользователь помилован!')

        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif message.text == 'Далее':
        await settings_module(message, 2)

    elif message.text == 'Отмена':
        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)
    else:
        await message.answer('Нет такого варианта!')


async def unblock(message: types.Message):
    if message.text == 'Разблокировать':
        DataBaseWork().delete_user_from_violators_table(DataBaseWork().get_data_from_admins_table('violators_id', message.from_user.id))
        await message.answer('Пользователь разблокирован!')

        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)

    elif message.text == 'Далее':
        await settings_module(message, 3)

    elif message.text == 'Отмена':
        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)
    else:
        await message.answer('Нет такого варианта!')

async def output_from_profile(self_id, violator_id):
    photo_or_video_id = DataBaseWork().get_data_from_profiles_table('photo_or_video_id', violator_id)

    if DataBaseWork().get_data_from_profiles_table('description', violator_id) == '':
        str = f"{DataBaseWork().get_data_from_profiles_table('user_name', violator_id)}, " \
              f"{DataBaseWork().get_data_from_profiles_table('age', violator_id)}, " \
              f"{DataBaseWork().get_data_from_profiles_table('city', violator_id)}." \
              f"{DataBaseWork().get_data_from_profiles_table('dop_info', violator_id)}"

    else:
        str = f"{DataBaseWork().get_data_from_profiles_table('user_name', violator_id)}, " \
              f"{DataBaseWork().get_data_from_profiles_table('age', violator_id)}, " \
              f"{DataBaseWork().get_data_from_profiles_table('city', violator_id)} - " \
              f"{DataBaseWork().get_data_from_profiles_table('description', violator_id)}.\n" \
              f"{DataBaseWork().get_data_from_profiles_table('dop_info', violator_id)}"


    try:
        await bot.send_photo(chat_id=self_id, photo=photo_or_video_id, caption=str)

    except:
        await bot.send_video(chat_id=self_id,video=photo_or_video_id, caption=str)
'''******************************************************************************************************************'''

'''*** Функциональный блок "Аналитика" ***'''
'''******************************************************************************************************************'''
async def analytics(msg):
    await msg.answer(f'Активных пользователей: {DataBaseWork().get_active_users()}\n'
                     f'Всего пользователей: {DataBaseWork().get_all_users_id()}', reply_markup=buttons.inline_markup_excel)

    await admin_menu_module(msg)

async def is_output_excel(callback: types.CallbackQuery):
    DataBaseWork().read_sql_to_frame()
    try:
        await callback.message.answer_document(open('Статистика.xlsx', 'rb'))
    except:
        pass

    os.remove('Статистика.xlsx')
'''******************************************************************************************************************'''

async def is_menu(message: types.Message):
    if DataBaseWork().is_user_blocked(message.from_user.id) == False:
        if message.text == '/start':
            await start_bot.command_start_module(message)

# Функция регистрации хэндлеров файла "admins.py"
def reg_handlers_questionnaire(dp: Dispatcher):
    dp.register_message_handler(first_chocie_handler, state=AdminStates.first_choice)

    dp.register_message_handler(from_user_to_admin, state=AdminStates.user_to_admin)
    dp.register_message_handler(from_admin_to_user, state=AdminStates.admin_to_user)

    dp.register_message_handler(mailing_choice, state=AdminStates.mailing_choice)
    dp.register_message_handler(choise_sex_for_mailing_to_specific, state=AdminStates.choise_sex)
    dp.register_message_handler(get_mail_from_admin, state=AdminStates.get_mail, content_types=['photo', 'video', 'text'])
    dp.register_message_handler(save_mail, state=AdminStates.save_mail)
    dp.register_message_handler(send_out_mail, state=AdminStates.send_out_mail)

    dp.register_message_handler(settings_handler, state=AdminStates.settings)
    dp.register_message_handler(warn, state=AdminStates.settings_warn)
    dp.register_message_handler(block, state=AdminStates.settings_block)
    dp.register_message_handler(unblock, state=AdminStates.settings_unblock)

    dp.register_callback_query_handler(is_output_excel, Text('output_excel'), state=AdminStates.all_states)
    dp.register_message_handler(is_menu, state=AdminStates.all_states)
