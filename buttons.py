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

numbers = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(KeyboardButton('1'),
                                                                                KeyboardButton('2'),
                                                                                KeyboardButton('3'),
                                                                                KeyboardButton('4 🚀'))

'''***** Кнопки для меню обычного пользователя после заполнения анкеты*****'''
menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu.row(KeyboardButton('💌 Тиндер'), KeyboardButton('👤 Мой профиль'))
menu.add(KeyboardButton('🙋‍♀ Поддержка️'))


'''***** Кнопки для реакции на анкету *****'''
inline_btn1 = InlineKeyboardButton(text='👍', callback_data='👍',)
inline_btn2 = InlineKeyboardButton(text='👎', callback_data='👎')
inline_markup = InlineKeyboardMarkup(row_width=2).add(inline_btn1, inline_btn2)

'''***** Кнопки для выбора режима *****'''
mode = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mode.add(KeyboardButton('Обычный пользователь'))
mode.add(KeyboardButton('Администратор'))

'''***** Кнопки для стартового меню администратора *****'''
start_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_admin_menu.add(KeyboardButton('📣 Сделать рассылку пользователям'))
start_admin_menu.row(KeyboardButton('⚙ Настройки'), KeyboardButton('🗂 Аналитика'))
start_admin_menu.add(KeyboardButton('🔙 Вернуться к выбору режима'))

'''***** Кнопки для меню администратора (Рассылка)*****'''
mailing_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mailing_admin_menu.add(KeyboardButton('🔔 Обычная рассылка'))
mailing_admin_menu.add(KeyboardButton('👥 Конкретным пользователям'))
mailing_admin_menu.add(KeyboardButton('🔙 Вернуться к меню администратора'))

cancel = KeyboardButton('Отмена')
cancel_reply = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cancel)

mailing_specific = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
mailing_specific.row(KeyboardButton('Девушкам'), KeyboardButton('Парням'))
mailing_specific.add(cancel)

'''***** Кнопки для меню администратора (Настройки)*****'''
settings_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_admin_menu.row(KeyboardButton('Предупредить'), KeyboardButton('Заблокировать'))
settings_admin_menu.add(KeyboardButton('Разблокировать пользователя'))
settings_admin_menu.add(KeyboardButton('Назад'))

'''***** Кнопки для меню администратора (Аналитика)*****'''
