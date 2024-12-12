from aiogram import Bot, Dispatcher, types
from dotenv import dotenv_values
from aiogram.filters import Command



token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()