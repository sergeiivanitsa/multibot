import aiohttp
import requests
from aiogram import types, Dispatcher
from create_bot import dp
import os
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
EX_API_KEY = os.getenv('EX_API_KEY')
print(EX_API_KEY)

#@dp.message_handler()
#@dp.message_handler(lambda message: message.text and 'hello' in message.text.lower())
async def get_weather(message: types.Message):
    try:
        print(message.text)
        command, city = message.text.split()[1:]
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        await message.reply(
            f"Погода в городе: {city}\nТемпература: {cur_weather}C°\n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
        )
    except Exception as e:
        await message.reply(
            f"Ошибка в {e}")


'''***********************КОНВЕРТЕР_ВАЛЮТ************************'''


async def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={target_currency}") as response:
            data = await response.json()
            return data["rates"][target_currency]


async def convert_currency(base_currency: str, amount: float, target_currency: str) -> float:
    exchange_rate = await get_exchange_rate(base_currency, target_currency)
    return amount * exchange_rate


async def get_currency(message: types.Message):
    try:
        base_currency, amount, target_currency = message.text.split()[1:]
        amount = float(amount)
        result = await convert_currency(base_currency.upper(), amount, target_currency.upper())
        await message.answer(f"{amount} {base_currency.upper()} = {result} {target_currency.upper()}")
    except ValueError:
        await message.answer("Invalid format. Please use the following format: /currency BASE_AMOUNT TARGET")
    except KeyError:
        await message.answer("Invalid currency code. Please use valid ISO 4217 currency codes.")


async def currency_conversion(message: types.Message):
    try:
        basecurrency, amount, targetcurrency = message.text.split()[0:]
        amount = float(amount)
        async with aiohttp.ClientSession() as session:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to={targetcurrency}&from={basecurrency}&amount={amount}"
            headers = {
                "apikey": EX_API_KEY
            }
            payload = {}
            async with session.get(url, headers=headers, data=payload) as response:
                data = await response.json()
                exchangerate = data["result"]
        result = exchangerate
        await message.answer(f"{amount} {basecurrency.upper()} = {result} {targetcurrency.upper()}")
    except ValueError:
        await message.answer("Неверный формат ввода")
    except KeyError:
        await message.answer("Неверный код валюты")


'''***********************КОНЕЦ_КОНВЕРТЕРА_ВАЛЮТ************************'''


def register_handlers_other(dp: Dispatcher):
    #dp.register_message_handler(get_weather)
    dp.register_message_handler(currency_conversion, regexp='\w{3}\s\d+\s\w{3}')
    dp.register_message_handler(get_weather, lambda message: message.text and 'погода' in message.text.lower(), state="*")
