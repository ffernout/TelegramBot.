from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router
import sqlite3

admin_module = Router()

ADMIN_ID = 1654851552

class AddingDishes(StatesGroup):
    name_dishes = State()
    price = State()
    description = State()
    category = State()

def save_dish_to_db(name, price, description, category):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO dishes (name, price, description, category)
    VALUES (?, ?, ?, ?)
    ''', (name, price, description, category))
    conn.commit()
    conn.close()

async def add_dish_start(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет прав для добавления блюд.")
        return

    await AddingDishes.name_dishes.set()
    await message.answer("Введите название блюда:")


async def process_dish_name(message: types.Message, state: FSMContext):
    dish_name = message.text
    await state.update_data(dish_name=dish_name)

    await AddingDishes.price.set()
    await message.answer("Введите цену блюда:")

async def process_dish_price(message: types.Message, state: FSMContext):
    try:
        dish_price = float(message.text)
        await state.update_data(dish_price=dish_price)

        await AddingDishes.description.set()
        await message.answer("Введите описание блюда:")
    except ValueError:
        await message.answer("Пожалуйста, введите корректную цену.")


async def process_dish_description(message: types.Message, state: FSMContext):
    dish_description = message.text
    await state.update_data(dish_description=dish_description)

    await AddingDishes.category.set()
    await message.answer(
        "Выберите категорию блюда:\n1. Супы\n2. Вторые\n3. Горячие напитки\n4. Холодные напитки"
    )

async def process_dish_category(message: types.Message, state: FSMContext):
    category_map = {
        "1": "Супы",
        "2": "Вторые",
        "3": "Горячие напитки",
        "4": "Холодные напитки"
    }

    category = message.text.strip()
    if category in category_map:
        user_data = await state.get_data()
        dish_name = user_data.get('dish_name')
        dish_price = user_data.get('dish_price')
        dish_description = user_data.get('dish_description')
        dish_category = category_map[category]

        save_dish_to_db(dish_name, dish_price, dish_description, dish_category)

        await message.answer(f"Блюдо '{dish_name}' добавлено:\n"
                             f"Цена: {dish_price} руб.\n"
                             f"Описание: {dish_description}\n"
                             f"Категория: {dish_category}")
        await state.finish()
    else:
        await message.answer("Неверный выбор категории. Пожалуйста, выберите правильную категорию.")

