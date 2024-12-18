from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
import sqlite3

questions_router = Router()

class Questions(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


def create_table():
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


create_table()

def save_review(name, phone_number, food_rating, cleanliness_rating, extra_comments):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO reviews (name, phone_number, food_rating, cleanliness_rating, extra_comments)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, phone_number, food_rating, cleanliness_rating, extra_comments))

    conn.commit()
    conn.close()
