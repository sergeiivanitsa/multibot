from aiogram import types, Dispatcher
from create_bot import dp
from handlers.other import currency_conversion


#@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Выбери одну из функций!"
                        )


#@dp.message_handler(commands=['weather'])
async def weather_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")


async def currency_command(message: types.Message):
    await message.reply("Это конвертер валют, введите начальную валюту, сумму и квалюту конвертации. К примеру USD 100 EUR")


def register_handlers_clients(dp):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(weather_command, commands=['weather'])
    #dp.register_message_handler(currency_command, commands=['currency'])
