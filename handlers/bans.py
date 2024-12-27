import logging
from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

BANNED_WORDS = ["найк про", "босс художки", "пикми"]

async def check_for_banned_words(message: Message, state: FSMContext):
    text = message.text.lower()

    for banned_word in BANNED_WORDS:
        if banned_word in text:
            try:
                await message.chat.kick_member(message.from_user.id)
                await message.answer(f"Ай-ай-ай, такие слова писать нельзя..")
                logging.info(f"Пользователь {message.from_user.id} заблокирован за слово: {banned_word}")
            except Exception as e:
                logging.error(f"Ошибка при бане пользователя: {e}")
            return

