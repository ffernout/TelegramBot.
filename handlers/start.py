from aiogram import Router, types, F
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def start_command(message: types.Message):
    name = message.from_user.first_name
    kb = types.ReplyKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Как с нами связаться: ",
                                           url="https://telegram.нет_ссылки)"),
                types.InlineKeyboardButton(text="О нас: ", callback_data="about_us")


            ]
        ]
    )
    await message.answer(f"Привет, {name}! Я assistant_bot.", reply_markup=kb)


@start_router.callback_query(F.data == "about_us")
async def about_us(callback: types.CallbackQuery):
    await callback.answer("О нас: ")