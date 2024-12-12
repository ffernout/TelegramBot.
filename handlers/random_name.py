import random
from aiogram import types, Router
from aiogram.filters import Command

random_name_router = Router()


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


@random_name_router.message(Command("randomname"))
async def random_name_command(message: types.Message):
    await random_name(message)

@random_name_router.message(Command("myinfo"))
async def myinfo_command(message: types.Message):
    await myinfo(message)