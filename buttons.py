from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

'''***** Кнопка для удаления кнопок *****'''
remove_markup = ReplyKeyboardRemove()

'''***** Кнопки для создания/редактирования анкеты *****'''
sex = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Я девушка'),
                                                                            KeyboardButton('Я парень'))

who_do_you_like = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Девушки'),
                                                                                        KeyboardButton('Парни'),
                                                                                        KeyboardButton('Все равно'))

description_of_yourself = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Пропустить'))

yes_or_no = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Да'),
                                                                                  KeyboardButton('Изменить анкету'))

numbers = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
numbers.row(KeyboardButton('1'),
            KeyboardButton('2'),
            KeyboardButton('3'))
numbers.row(KeyboardButton('4'),
            KeyboardButton('5'),
            KeyboardButton('6'))
numbers.row(KeyboardButton('7 🚀'))

'''***** Кнопки для меню обычного пользователя после заполнения анкеты*****'''
menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu.row(KeyboardButton('Найти друга'), KeyboardButton('👤 Мой профиль'))
menu.row(KeyboardButton('⛔ Скрыть анкету'), KeyboardButton('⛑ Проблема с ботом'))

menu_close = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_close.row(KeyboardButton('Найти друга'), KeyboardButton('👤 Мой профиль'))
menu_close.add(KeyboardButton('⛑ Проблема с ботом'))


'''***** Кнопки для администратора после заполнения/оценки анкеты*****'''
menu_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_admin.row(KeyboardButton('Найти друга'), KeyboardButton('👤 Мой профиль'))
menu_admin.add(KeyboardButton('⛔ Скрыть анкету'), KeyboardButton('⛑ Проблема с ботом'))
menu_admin.add(KeyboardButton('Выбор режима'))

menu_admin_close = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu_admin_close.row(KeyboardButton('Найти друга'), KeyboardButton('👤 Мой профиль'))
menu_admin_close.add(KeyboardButton('⛑ Проблема с ботом'))
menu_admin_close.add(KeyboardButton('Выбор режима'))


'''***** Кнопки для реакции на анкету *****'''
inline_btn1 = InlineKeyboardButton(text='👍', callback_data='👍',)
inline_btn2 = InlineKeyboardButton(text='👎', callback_data='👎')
inline_btn3 = InlineKeyboardButton(text='Пожаловаться', callback_data='complain')
inline_markup = InlineKeyboardMarkup(row_width=2).add(inline_btn1, inline_btn2, inline_btn3)

'''***** Кнопки для выбора режима *****'''
mode = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mode.add(KeyboardButton('Обычный пользователь'))
mode.add(KeyboardButton('Администратор'))

'''***** Кнопки для стартового меню администратора *****'''
start_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_admin_menu.add(KeyboardButton('📣 Сделать рассылку пользователям'))
start_admin_menu.row(KeyboardButton('⚙ Настройки'), KeyboardButton('🗂 Аналитика'))
start_admin_menu.add(KeyboardButton('🔙 Вернуться к выбору режима'))
start_admin_menu.add(KeyboardButton('Повысить до администратора'))
start_admin_menu.add(KeyboardButton('Понизить до обычного пользователя'))

'''***** Кнопки для меню администратора (Рассылка)*****'''
mailing_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mailing_admin_menu.add(KeyboardButton('🔔 Обычная рассылка'))
mailing_admin_menu.add(KeyboardButton('👥 Конкретным пользователям'))
mailing_admin_menu.add(KeyboardButton('🔙 Вернуться в меню'))

cancel = KeyboardButton('Отмена')
cancel_reply = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cancel)

mailing_specific = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mailing_specific.row(KeyboardButton('Девушкам'), KeyboardButton('Парням'))
mailing_specific.add(cancel)

'''***** Кнопки для меню администратора (Настройки)*****'''
settings_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_admin_menu.row(KeyboardButton('Предупредить'), KeyboardButton('Заблокировать'))
settings_admin_menu.add(KeyboardButton('Разблокировать пользователя'))
settings_admin_menu.add(KeyboardButton('🔙 Вернуться в меню'))

settings_warn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Предупредить'), KeyboardButton('Помиловать'))
settings_warn.add(KeyboardButton('Далее'))
settings_warn.add(KeyboardButton('Отмена'))

settings_block = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Заблокировать'), KeyboardButton('Помиловать'))
settings_block.add(KeyboardButton('Далее'))
settings_block.add(KeyboardButton('Отмена'))

settings_unblock = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Разблокировать'))
settings_unblock.add(KeyboardButton('Далее'))
settings_unblock.add(KeyboardButton('Отмена'))


'''***** Кнопки для меню администратора (Аналитика)*****'''
inline_excel = InlineKeyboardButton(text='Выгрузить Excel файл', callback_data='output_excel')
inline_markup_excel = InlineKeyboardMarkup(row_width=1).add(inline_excel)




da = InlineKeyboardButton(text='Да', callback_data='yes_show_me')
net = InlineKeyboardButton(text='Нет', callback_data='dont_show_me')

da_net = InlineKeyboardMarkup(row_width=2).add(da,net)


view = InlineKeyboardButton(text='Показать профиль', callback_data='view')

view_markup = InlineKeyboardMarkup(row_width=1).add(view)

save_or_no = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('Сохранить'), cancel)

yes_or_no_send_mail = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('✅ Да'), KeyboardButton('❎ Нет'))