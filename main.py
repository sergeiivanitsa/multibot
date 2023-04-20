import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
import requests

logging.basicConfig(level=logging.INFO)

bot = Bot(token='6275097818:AAFZFRqnuSNWOHFnQsXy7r6iyZ1bd15I4Ww')
API_KEY = 'df89fa95364b84b339f83db2404e8ff7'

dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await set_commands(bot)
    await message.reply("Привет! Выбери одну из функций!"
                        )


@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(message.text)


async def weather_command(message: types.Message):
    await message.answer("Введите город:")
    # ждем ответа от пользователя
    city = await bot.wait_for('message')
    # отправляем запрос на openweathermap.org для получения погоды в указанном городе
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city.text}&appid={API_KEY}&units=metric')
    if response.status_code == 200:
        # извлекаем данные о погоде из ответа и формируем сообщение для отправки пользователю
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        message_text = f"Погода в городе {city.text}: {temp}°C, {description}"
        await message.answer(message_text)
    else:
        await message.answer("Не удалось получить данные о погоде")

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

async def set_commands(bot):
    commands = [
        types.BotCommand(
            command='weather',
            description='погода'
        )
    ]

    await bot.set_my_commands(commands, types.BotCommandScopeDefault)

dp.register_message_handler(weather_command, Command("узнать_погоду"))
dp.register_message_handler(exchange_rate_command, Command("узнать_курс_валют"))
dp.register_message_handler(get_image_command, Command("получить_картинку"))
dp.register_message_handler(create_poll_command, Command("создать_опрос"))


if __name__ == '__main__':
    logging.info("Starting bot")
    executor.start_polling(dp, skip_updates=True)
