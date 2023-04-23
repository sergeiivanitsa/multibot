import logging
import os
from dotenv import load_dotenv
from create_bot import dp

load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
EX_API_KEY = os.getenv('EX_API_KEY')

from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

from handlers import client, other

client.register_handlers_clients(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    logging.info("Starting bot")
    executor.start_polling(dp, skip_updates=True)
