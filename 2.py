import aiohttp
from aiogram import types
from aiogram.dispatcher.filters import Command


async def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={target_currency}") as response:
            data = await response.json()
            return data["rates"][target_currency]


async def convert_currency(base_currency: str, amount: float, target_currency: str) -> float:
    exchange_rate = await get_exchange_rate(base_currency, target_currency)
    return amount * exchange_rate


async def currency_command(message: types.Message):
    try:
        base_currency, amount, target_currency = message.text.split()[1:]
        amount = float(amount)
        result = await convert_currency(base_currency.upper(), amount, target_currency.upper())
        await message.answer(f"{amount} {base_currency.upper()} = {result} {target_currency.upper()}")
    except ValueError:
        await message.answer("Invalid format. Please use the following format: /currency BASE_AMOUNT TARGET")
    except KeyError:
        await message.answer("Invalid currency code. Please use valid ISO 4217 currency codes.")


def register_handlers(dp):
    dp.register_message_handler(currency_command, Command("currency"))
