from aiogram import Dispatcher, Bot
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
