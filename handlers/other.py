import aiohttp
import requests
from aiogram.dispatcher.filters import Text

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


"""************************************_Опросы_Polls_************************************"""

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types


class FSMPolls(StatesGroup):
    question = State()
    answers = State()
    chatlink = State()


# Ловим ответ
async def catch_options(message: types.Message):
    text = await message.text
    return text


# Начало диалога создания
#@dp.message_handler(commands='/polls', state=None)
async def polls_start_command(message: types.Message):
    await FSMPolls.question.set()
    await message.reply('Укажи вопрос')


# Ловим ответ и пишем в словарь
#@dp.message_handler(state=FSMPolls.question)
async def catch_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
    await FSMPolls.next()
    await message.reply('Теперь введи количество ответов')


# Ловим варианты ответов
#@dp.message_handler(state=FSMPolls.answers)
async def catch_answers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        num_options = int(message.text)
    answers = []
    for num in range(num_options):
        await message.reply(f'Укажи ответ на вопрос номер {num}')
        answer = await catch_options(message)
        answers.append(answer)
    data['answers'] = answers
    await FSMPolls.next()
    await message.reply('Укажи ссылку на чат, куда нужно отправить опрос')


# Выход из состояний
#@dp.message_handler(state='*', commands='отмена')
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


# Выход из состояний
#@dp.message_handler(state=FSMPolls.chatlink)
async def catch_chatlink(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['chatlink'] = message.text

    # здесь реализовать отпрвку опроса в чат
    # async def start_command(message: types.Message):

    poll = types.Poll(
        question=data['question'],
        options=data['answers'],
        type=types.PollType.REGULAR,
        is_anonymous=False)

    await bot.send_poll(chat_id=message.chat.id, poll=poll)
    await state.finish()


"""*********************************_Конец_Опросов_Polls_*********************************"""


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(currency_conversion, regexp='\w{3}\s\d+\s\w{3}')
    dp.register_message_handler(get_weather, lambda message: message.text and 'погода' in message.text.lower(),
                                state="*")
    dp.register_message_handler(polls_start_command, commands='/polls', state=None)
    dp.register_message_handler(catch_question, state=FSMPolls.question)
    dp.register_message_handler(catch_answers, state=FSMPolls.answers)
    dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(catch_chatlink, state=FSMPolls.chatlink)

