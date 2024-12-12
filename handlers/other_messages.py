from aiogram import Router, types


other_echo_handler = Router()

@other_echo_handler.message()
async def echo_handler(message: types.Message):
    txt = message.text
    await message.answer(f"Вы сказали: {txt}")
    await message.bot.send_message(
        chat_id = message.from_user.id,
        text="Команда неопоздана."
    )