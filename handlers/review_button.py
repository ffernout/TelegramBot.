from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


review_button = Router()


class Review(StatesGroup):
    name = State()


@review_button.callback_query(F.data == "review")
async def start_review(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Напишите отзыв")
    await state.set_state(Review.name)