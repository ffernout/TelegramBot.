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
            ],
            [
                types.InlineKeyboardButton(text="Оставить отзыв.", callback_data="review"),

            ]
        ]
    )
    await message.answer(f"Привет, {name}! Я assistant_bot.", reply_markup=kb)


@start_router.callback_query(F.data == "about_us")
async def about_us(callback: types.CallbackQuery):
    await callback.answer("О нас: ")


@start_router.message(Command('menu'))
async def menu_command(message: types.Message):
    await show_dishes(message)


def get_all_dishes():
    pass


async def show_dishes(message: types.Message):
    dishes = get_all_dishes()

    if not dishes:
        await message.answer("Извините, блюда не найдены.")
        return

    dishes_text = ""
    for dish in dishes:
        name, description, price, category = dish
        dishes_text += f"🍽️ <b>{name}</b>\n"
        dishes_text += f"📝 Описание: {description}\n"
        dishes_text += f"💲 Цена: {price} руб.\n"
        dishes_text += f"🍴 Категория: {category}\n\n"

    await message.answer(dishes_text, parse_mode="HTML")



