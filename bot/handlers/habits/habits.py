from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.habits.habit_kb import get_start_habit

router = Router()


@router.message(F.text == "📈 Трекер привычек")
async def enter_habits(message: Message):
    await message.answer(
        text=(
            "<strong>📈 Трекер привычек</strong>\n\n"
            "Здесь ты можешь:\n"
            "• создавать привычки 🧠\n"
            "• отмечать выполнение ✅\n"
            "• следить за прогрессом и стриком 🔥\n\n"
            "Выбери действие ниже ⬇️"
        ),
        reply_markup=get_start_habit(),
    )
