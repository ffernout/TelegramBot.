from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


opros_router = Router()

class opros(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@opros_router.message(Command("opros"))
async def start_opros(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Как вас зовут?")
    await state.set_state(opros.name)

@opros_router.message(opros.name)
async def phone_number(message: types.Message, state: FSMContext):
    await message.answer("Как с вами можно связаться?")
    await state.set_state(opros.phone_number)

@opros_router.message(opros.phone_number)
async def food_rating(message: types.Message, state: FSMContext):
    await message.answer("Какую оценку поставите нашей пиццерии? от 1 до 10")
    await state.set_state(opros.food_rating)

@opros_router.message(opros.food_rating)
async def cleanliness_rating(message: types.Message, state: FSMContext):
    food_rating = message.text
    if not food_rating.isdigit():
        await message.answer("Введите число от 1 до 10")
        return
    food_rating = int(food_rating)
    if food_rating < 1 or food_rating > 10:
        return
    await message.answer("Как оцениваете чистоту заведения? от 1 до 10")
    await state.set_state(opros.cleanliness_rating)

@opros_router.message(opros.cleanliness_rating)
async def extra_comments(message: types.Message, state: FSMContext):
    cleanliness_rating = message.text
    if not cleanliness_rating.isdigit():
        await message.answer("Введите число от 1 до 10")
        return
    cleanliness_rating = int(cleanliness_rating)
    if cleanliness_rating < 1 or cleanliness_rating > 10:
        return

    await message.answer("Дополнительные комментарии/жалоба?")
    await state.set_state(opros.extra_comments)

@opros_router.message(opros.cleanliness_rating)

async def comments(message: types.Message, state: FSMContext):
    await state.update_data(comments=message.text)
    data = await state.get_data()
    await message.answer(f"Спасибо за ваш отзыв, {data['name']}!\n"
                         f"Способ связи: {data['phone_number']}\n"
                         f"Оценка еды: {data['food_rating']}\n"
                         f"Оценка чистоты: {data['cleanliness_rating']}\n"
                         f"Дополнительные комментарии/жалобы: {data['extra_comments']}")
    await state.clear()
