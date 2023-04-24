from aiogram import types, Dispatcher
from create_bot import dp
from .other import send_cat_picture


async def start_command(message: types.Message):
    """Функция ответа на команду /start"""
    await message.reply("Привет! Выбери одну из функций!\n\n"
                        "1. Чтобы узнать погоду в любом городе планеты"
                        " отправь слово погода и укажи город."
                        " Например 'Погода Москва' или 'Погода Биробиджан'\n\n"
                        "2. Чтобы конвертировать валюту укажи трехбуквенный\n"
                        "код исходной валюты, сумму и трехбуквенный код\n"
                        "конечной валюты. Например 'USD 100 EUR'\n\n"
                        "3. Чтобы получить смешную картинку с котиками отправь команду /picture")


async def picture_command(message: types.Message):
    """Функция отправки картинки на команду /picture"""
    await send_cat_picture(message)


def register_handlers_clients(dp):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(picture_command, commands=['picture'])
