from aiogram import types
from aiogram.utils import executor
from create_bot import dp
from work_with_db import DataBaseWork


'''Нажатие кнопки получение реферальной системы'''
@dp.message_handler(commands='run')
async def make_referral_url(message: types.Message):
    user_ID = message.from_user.id
    url = f'https://t.me/OkDescRetaker_bot?start={user_ID}'
    await message.answer(f'{url}')
    await message.answer('Это ваша реферальная ссылка\nПришлите ее другу\nПосле его регистрации, вы получите бонус')

@dp.message_handler(commands='start')
async def command_start_from_referrer(message: types.Message):
    try:
        user_id_owner = message.text.split()[1]
        await message.answer('Реферальный старт')
        user_id_referral = message.from_user.id
        if DataBaseWork.is_exist_user_in_db('',user_id=user_id_referral) == True:
            message.answer('Реферальная система сработала')
        else:
            await message.answer('Пользователь уже зарегестрирован')
    except IndexError:
        pass
        await message.answer('Обычный старт')

executor.start_polling(dp, skip_updates=True)