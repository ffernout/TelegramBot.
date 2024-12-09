from aiogram import Bot, Dispatcher, types
import asyncio
from dotenv import dotenv_values
from aiogram.filters import Command
import random


token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()

NAME = ("Максим", "Мэри", "Джеймс", "Лора", "Анжела")


async def random_name(message: types.Message):
    random_choice = random.choice(NAME)
    await message.reply(f"Случайное имя: {random_choice}")

async def myinfo(message: types.Message):
    user = message.from_user
    user_info = (
        f"Ваше ID: {user.id}\n"
        f"Ваше имя: {user.first_name}\n"
        f"Ваше имя пользователя: @{user.username}"
    )
    await message.answer(user_info)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    name = message.from_user.first_name
    await message.answer(f"Привет, {name}! Я assistant_bot.")

@dp.message()
async def echo_handler(message: types.Message):
    txt = message.text
    await message.answer(f"Вы сказали: {txt}")

@dp.message(Command("randomname"))
async def random_name_command(message: types.Message):
    await random_name(message)

@dp.message(Command("myinfo"))
async def myinfo_command(message: types.Message):
    await myinfo(message)

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())