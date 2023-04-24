import aiohttp
import requests
from create_bot import bot
from aiogram import types, Dispatcher, Bot
from aiogram.utils import exceptions
from transliterate import translit
from create_bot import dp
import os
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
EX_API_KEY = os.getenv('EX_API_KEY')


async def get_weather(message: types.Message):
    """Функция для запроса погоды в городе через api openweathermap"""
    try:
        # Получаем город
        command, city_ru = message.text.split()[0:]
        # Переписываем город английскими буквами
        city_en = translit(city_ru, language_code='ru', reversed=True)
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_en}&appid={WEATHER_API_KEY}&units=metric"
        )
        data = r.json()
        city = translit(data["name"], 'ru')
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        await message.reply(
            f"Погода в городе: {city}\nТемпература: {cur_weather}C°\n"
            f"Влажность: {humidity}%\nВетер: {wind} м/с\n"
        )
    except Exception as e:
        await message.reply(
            f"Ошибка в {e}")


async def get_cat_picture():
    """Функция для запроса картинки через API сайта thecatapi.com"""
    async with aiohttp.ClientSession() as session:
        # Делаем запрос к API
        async with session.get('https://api.thecatapi.com/v1/images/search') as response:
            # Сохраняем ответ в json
            data = await response.json()
            return data


async def send_cat_picture(message: types.Message):
    """Функция для отправки сообщения с картинкой котика пользователю"""
    try:
        # Получаем картинку с эндпоинта
        data = await get_cat_picture()
        if data:
            # Парсим URL картинки
            url = data[0]['url']
            # Отправляем картинку пользователю
            await bot.send_photo(chat_id=message.chat.id, photo=url)
        else:
            await message.reply('Не удалось получить картинку')
    except exceptions.MessageTextIsEmpty:
        await message.reply('Не удалось получить картинку')


async def currency_conversion(message: types.Message):
    """Функция конвертации суммы из одной валюты в другую"""
    try:
        # Записываем валюты и сумму в переменные
        basecurrency, amount, targetcurrency = message.text.split()[0:]
        amount = float(amount)
        async with aiohttp.ClientSession() as session:
            # Формируем запрос к API на конвертацию
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={targetcurrency}&from={basecurrency}&amount={amount}"
            headers = {
                "apikey": EX_API_KEY
            }
            # Осуществляем запрос к API
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                exchangerate = data["result"]
        # Формируем ответ
        await message.answer(f"{amount} {basecurrency.upper()} = {exchangerate} {targetcurrency.upper()}")
    except ValueError:
        await message.answer("Неверный формат ввода")
    except KeyError:
        await message.answer("Неверный код валюты")


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(currency_conversion, regexp='\w{3}\s\d+\s\w{3}')
    dp.register_message_handler(get_weather, lambda message: message.text and 'погода' in message.text.lower(), state="*")
