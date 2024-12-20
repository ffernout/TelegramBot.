from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
import sqlite3
from aiogram.fsm.context import FSMContext

questions_router = Router()

class Questions(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


def create_tables():

    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        food_rating INTEGER NOT NULL,
        cleanliness_rating INTEGER NOT NULL,
        extra_comments TEXT,
        created_at DATE DEFAULT (CURRENT_DATE)
    )
    ''')

    conn.commit()
    conn.close()


create_tables()

def save_review(name, phone_number, food_rating, cleanliness_rating, extra_comments):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO reviews (name, phone_number, food_rating, cleanliness_rating, extra_comments)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, phone_number, food_rating, cleanliness_rating, extra_comments))

    conn.commit()
    conn.close()

async def save_review(message: types.Message, state: FSMContext):
    extra_comments = message.text
    await state.update_data(extra_comments=extra_comments)

    data = await state.get_data()

    save_review(
        name=data['name'],
        phone_number=data['phone_number'],
        food_rating=data['food_rating'],
        cleanliness_rating=data['cleanliness_rating'],
        extra_comments=data['extra_comments']
    )

State.clear()