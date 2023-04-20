import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def weather_command(message: types.Message):
    # здесь должен быть код для получения погоды
    await message.answer("Сейчас погода ...")

async def exchange_rate_command(message: types.Message):
    # здесь должен быть код для получения курса валют
    await message.answer("Курс доллара к рублю сейчас ...")

async def get_image_command(message: types.Message):
    # здесь должен быть код для получения картинки
    with open('image.jpg', 'rb') as photo:
        await message.answer_photo(photo)

async def create_poll_command(message: types.Message):
    # здесь должен быть код для создания опроса
    await message.answer("Опрос создан!")

dp.register_message_handler(weather_command, Command("узнать_погоду"))
dp.register_message_handler(exchange_rate_command, Command("узнать_курс_валют"))
dp.register_message_handler(get_image_command, Command("получить_картинку"))
dp.register_message_handler(create_poll_command, Command("создать_опрос"))

if __name__ == '__main__':
    logging.info("Starting bot")
    executor.start_polling(dp, skip_updates=True)