from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import sqlite3

review_button = Router()
questions_router = Router()

user = []

class Questions(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_button.message(Command("stop"))
@review_button.message(F.text == "стоп")
async def stop_reviews(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Диалог завершен.")

@questions_router.message(Questions.name)
async def ask_name(message: types.Message, state: FSMContext):
    await message.answer("Как вас зовут?")
    await state.set_state(Questions.phone_number)

@questions_router.message(Questions.phone_number)
async def ask_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Как с вами можно связаться?")
    await state.set_state(Questions.food_rating)

@questions_router.message(Questions.food_rating)
async def ask_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Какую оценку поставите нашей пиццерии? от 1 до 10")
    await state.set_state(Questions.cleanliness_rating)

@questions_router.message(Questions.cleanliness_rating)
async def ask_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    food_rating = message.text
    if not food_rating.isdigit():
        await message.answer("Введите число от 1 до 10")
        return
    food_rating = int(food_rating)
    if food_rating < 1 or food_rating > 10:
        await message.answer("Пожалуйста, введите число от 1 до 10.")
        return

    await message.answer("Как оцениваете чистоту заведения? от 1 до 10")
    await state.set_state(Questions.extra_comments)

@questions_router.message(Questions.extra_comments)
async def ask_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    cleanliness_rating = message.text
    if not cleanliness_rating.isdigit():
        await message.answer("Введите число от 1 до 10")
        return
    cleanliness_rating = int(cleanliness_rating)
    if cleanliness_rating < 1 or cleanliness_rating > 10:
        await message.answer("Пожалуйста, введите число от 1 до 10.")
        return

    await message.answer("Дополнительные комментарии/жалоба?")
    await state.set_state(Questions.extra_comments)

@questions_router.message(Questions.extra_comments)
async def finalize_review(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    data = await state.get_data()
    await message.answer(f"Спасибо за ваш отзыв, {data['name']}!\n"
                         f"Способ связи: {data['phone_number']}\n"
                         f"Оценка еды: {data['food_rating']}\n"
                         f"Оценка чистоты: {data['cleanliness_rating']}\n"
                         f"Дополнительные комментарии/жалобы: {data['extra_comments']}")

    await state.clear()

@review_button.callback_query(F.data == "review")
async def start_review(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer("Напишите отзыв")
    await state.set_state(Questions.name)

class Form(StatesGroup):
    name = State()
    description = State()
    price = State()

@review_button.message(Command('add_dish'))
async def cmd_add_dish(message: types.Message):
    await Form.name.set()
    await message.reply("Введите название блюда:")

@review_button.message(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await Form.description.set()
    await message.reply("Введите описание блюда:")

@review_button.message(state=Form.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await Form.price.set()
    await message.reply("Введите цену блюда:")

@review_button.message(state=Form.price)
async def process_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    description = data.get('description')
    try:
        price = float(message.text)
    except ValueError:
        await message.reply("Пожалуйста, введите корректную цену.")
        return

    await save_dish(name, description, price)

    await state.finish()
    await message.reply("Блюдо успешно добавлено!")

@review_button.message(Command('list_dishes'))
async def cmd_list_dishes(message: types.Message):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('SELECT name, description, price FROM dishes')
    dishes = cursor.fetchall()

    if dishes:
        response = "Список блюд:\n"
        for dish in dishes:
            response += f"Название: {dish[0]}, Описание: {dish[1]}, Цена: {dish[2]}\n"
    else:
        response = "Нет добавленных блюд."

    await message.reply(response)
    conn.close()

async def save_dish(name: str, description: str, price: float):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dishes (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        price REAL
    )''')

    cursor.execute('INSERT INTO dishes (name, description, price) VALUES (?, ?, ?)', (name, description, price))
    conn.commit()
    conn.close()

