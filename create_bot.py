from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv
load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')

bot = Bot(token=BOT_KEY)
dp = Dispatcher(bot)
