import buttons
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from work_with_db import db
from aiogram.dispatcher.filters import Text

class AdminStates(StatesGroup):
    admin_menu = State()

    first_change = State()

    mailing_to_subscribers = State()
    mailing_change = State()
    mailing_to_all_subscribers = State()
    change_specific_subscribers = State()
    mailing_to_specific_subscribers = State()

    settings = State()
    settings_change = State()

    analytics = State()



'''*** Главное меню администратора ***'''
'''******************************************************************************************************************'''
async def admin_menu_handler(message: types.Message):
    await admin_menu_module(message)

async def admin_menu_module(msg):
    await AdminStates.first_change.set()
    await msg.answer('Выберите действие:', reply_markup=buttons.start_admin_menu)

async def first_change_handler(message: types.Message):
    if message.text == '📣 Сделать рассылку пользователям':
        await AdminStates.mailing_to_subscribers.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)
    elif message.text == '⚙ Настройки':
        await AdminStates.settings.set()
        await message.answer('Выберите то, что хотите сделать:', reply_markup=buttons.settings_admin_menu)
    elif message.text == '🗂 Аналитика':
        await AdminStates.analytics.set()
        await analytics(message)
    elif message.text == '🔙 Вернуться к выбору режима':
        await message.answer('Выбор режима...')
    else:
        await message.answer('Нет такого варианта!')
'''******************************************************************************************************************'''

'''*** Меню выбор типа рассылки ***'''
'''******************************************************************************************************************'''
async def mailing_to_subscribers_handler(message: types.Message):
    if message.text == '🔔 Обычная рассылка':
        await AdminStates.mailing_to_all_subscribers.set()
        await message.answer('Напишите текст, который необходимо разослать:', reply_markup=buttons.cancel_reply)
    elif message.text == '👥 Конкретным пользователям':
        await AdminStates.change_specific_subscribers.set()
        await message.answer('Выберите кому надо разослать:', reply_markup=buttons.mailing_specific)
    elif message.text == '🔙 Вернуться к меню администратора':
        await admin_menu_module(message)
    else:
        await message.answer('Нет такого варианта!')

# Рассылка по всем пользователям
async def mailing_to_all_subscribers_handler(message: types.Message):
    if message.text == 'Отмена':
        await AdminStates.mailing_to_subscribers.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:',
                             reply_markup=buttons.mailing_admin_menu)
    else:
        all_id = db.get_all_users_id()
        for i in range(len(all_id)):
            try:
                await bot.send_message(chat_id=all_id[i], text=message.text)
            except:
                pass

        await AdminStates.mailing_to_subscribers.set()
        await message.answer('Рассылка завершена!')
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)

# Выбор параметра, исходя из которого происходит отправка конкретным пользователям
async def change_specific_subscribers_handler(message: types.Message):
    if message.text == 'Девушкам':
        db.set_data_in_table('mailing_to', 'Я девушка', message.from_user.id, 'admins')
        await AdminStates.mailing_to_specific_subscribers.set()
        await message.answer('Напишите текст, который необходимо разослать:')
    elif message.text == 'Парням':
        db.set_data_in_table('mailing_to', 'Я парень', message.from_user.id, 'admins')
        await AdminStates.mailing_to_specific_subscribers.set()
        await message.answer('Напишите текст, который необходимо разослать:', reply_markup=buttons.cancel_reply)
    elif message.text == 'Отмена':
        await AdminStates.mailing_to_subscribers.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:',
                             reply_markup=buttons.mailing_admin_menu)

    else:
        await message.answer('Нет такого варианта!')

# Рассылка конкретным пользователям
async def mailing_to_specific_subscribers_handler(message: types.Message):
    if message.text == 'Отмена':
        await AdminStates.mailing_to_subscribers.set()
        await message.answer('Выберите рассылку, которую вы хотите сделать:',
                             reply_markup=buttons.mailing_admin_menu)
    else:
        all_specifics_id = db.get_all_specific_users_id(db.get_data_from_admins_table('mailing_to', message.from_user.id))
        for i in range(len(all_specifics_id)):
            try:
                await bot.send_message(chat_id=all_specifics_id[i], text=message.text)
            except:
                pass

        await AdminStates.mailing_to_subscribers.set()
        await message.answer('Рассылка завершена!')
        await message.answer('Выберите рассылку, которую вы хотите сделать:', reply_markup=buttons.mailing_admin_menu)
'''******************************************************************************************************************'''

'''*** Меню выбора типа настройки ***'''
'''******************************************************************************************************************'''
async def settings_handler(message: types.Message):
    if message.text == 'Предупредить':
        pass
    if message.text == 'Заблокировать':
        pass
    if message.text == 'Разблокировать пользователя':
        pass
    if message.text == 'Назад':
        pass
'''******************************************************************************************************************'''

'''*** Функциональный блок "Аналитика" ***'''
'''******************************************************************************************************************'''
async def analytics(msg):
    users_counter = 0
    active_users_counter = 0

    all_id = db.get_all_users_id()
    for i in range(len(all_id)):
        try:
            if db.is_exist_user_in_db(all_id[i], 'admins') == False:
                msg_from_bot = await bot.send_message(chat_id=all_id[i], text='👋')
                await msg_from_bot.delete()
                active_users_counter = active_users_counter + 1
                users_counter = users_counter + 1
        except:
            users_counter = users_counter + 1

    await msg.answer(f'Активных пользователей: {active_users_counter}\n'
                     f'Всего пользователей: {users_counter}', reply_markup=buttons.inline_markup_excel)

async def is_output_excel(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer_document(open('Статистика.xlsx', 'rb'))
'''******************************************************************************************************************'''

# Функция регистрации хэндлеров файла "admins.py"
def reg_handlers_questionnaire(dp: Dispatcher):
    dp.register_message_handler(first_change_handler, state=AdminStates.first_change)

    dp.register_message_handler(mailing_to_subscribers_handler, state=AdminStates.mailing_to_subscribers)
    dp.register_message_handler(mailing_to_all_subscribers_handler, state=AdminStates.mailing_to_all_subscribers)
    dp.register_message_handler(change_specific_subscribers_handler, state=AdminStates.change_specific_subscribers)
    dp.register_message_handler(mailing_to_specific_subscribers_handler, state=AdminStates.mailing_to_specific_subscribers)

    dp.register_message_handler(settings_handler, state=AdminStates.settings)

    dp.register_callback_query_handler(is_output_excel, Text('output_excel'), state=AdminStates.analytics)
