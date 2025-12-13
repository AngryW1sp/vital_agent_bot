from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from bot.keyboards.habits.habit_kb import complete_kb
from bot.services.errors import BackendError, format_backend_error, reply_error
from bot.services.requests import HabitServiceClient
from bot.utils.progress import render_progress

router = Router()


@router.message(F.text == '✅ Сегодня')
async def get_today_habits(message: Message, habit_client: HabitServiceClient):
    try:
        request = await habit_client.get_today_habits()
        habits = [h for h in request if h.get("is_active") is True]

        if not habits:
            await message.answer(
                "🎉 На сегодня невыполненных привычек нет!\n"
                "Так держать 🔥",
            )
            return

        await message.answer(
            "🗓️ <strong>Невыполненные привычки на сегодня</strong>\n"
            "Выбери привычку и отметь выполнение ✅"
        )

        for result in habits:
            name = result.get("name", "Без названия")
            description = result.get("description") or "Без описания"
            text = (
                f"<strong>{name}</strong>\n\n"
                f"<em>{description}</em>\n\n"
                f"Прогресс:\n {render_progress(result['completed_days_count'])}"
            )
            await message.answer(text=text, reply_markup=complete_kb(result["id"]))

    except BackendError as e:
        await reply_error(message, format_backend_error(e))


@router.callback_query(F.data.startswith('complete_habit:'))
async def complete_today_habit(cb: CallbackQuery, habit_client: HabitServiceClient):
    habit_id = int(cb.data.split(":")[1])
    try:
        await habit_client.complete_habit(habit_id=habit_id)
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.answer("✅ Отмечено! Отличная работа 🔥", show_alert=False)
    except BackendError as e:
        await reply_error(cb, format_backend_error(e))
