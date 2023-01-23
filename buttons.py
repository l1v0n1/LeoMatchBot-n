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

'''***** Кнопки для меню *****'''
menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
menu.row(KeyboardButton('💌 Тиндер'), KeyboardButton('👤 Мой профиль'))
menu.add(KeyboardButton('🙋‍♀ Поддержка️'))


'''***** Кнопки для реакции на анкету *****'''
inline_btn1 = InlineKeyboardButton(text='👍', callback_data='👍',)
inline_btn2 = InlineKeyboardButton(text='👎', callback_data='👎')
inline_markup = InlineKeyboardMarkup(row_width=2).add(inline_btn1, inline_btn2)
