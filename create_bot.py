from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv
load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')

storage = MemoryStorage()

# Создаем экземпляр бота
bot = Bot(token=BOT_KEY)

# Создаем диспетчер
dp = Dispatcher(bot)
