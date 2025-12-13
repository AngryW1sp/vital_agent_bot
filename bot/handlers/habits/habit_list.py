from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.services.requests import HabitServiceClient
from bot.keyboards.habits.habit_kb import confirm_delete_kb, get_habits_kb
from bot.utils.progress import render_progress
from bot.services.errors import BackendError, format_backend_error, reply_error

router = Router()


class EditHabit(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()


@router.message(F.text == '📋 Все привычки')
async def get_my_habits(message: Message, habit_client: HabitServiceClient):
    try:
        request = await habit_client.get_habits()
        habits = [h for h in request if h.get("is_active") is True]

        if not habits:
            await message.answer(
                "📭 У тебя пока нет активных привычек.\n\n"
                "Нажми <strong>➕ Создать привычку</strong>, чтобы добавить первую 💪"
            )
            return

        await message.answer("📋 <strong>Твои привычки</strong>\nВыбери действие под нужной привычкой ⬇️")

        for result in habits:
            name = result.get("name", "Без названия")
            description = result.get("description") or "Без описания"
            text = (
                f"<strong>{name}</strong>\n\n"
                f"<em>{description}</em>\n\n"
                f"Прогресс:\n {render_progress(result['completed_days_count'])}"
            )
            await message.answer(text=text, reply_markup=get_habits_kb(result["id"]))

    except BackendError as e:
        await reply_error(message, format_backend_error(e))


@router.callback_query(F.data.startswith("habit_delete:"))
async def ask_delete_confirm(cb: CallbackQuery):
    habit_id = int(cb.data.split(":")[1])

    await cb.message.answer(
        "⚠️ <strong>Удалить привычку?</strong>\n\n"
        "Это действие нельзя отменить.",
        reply_markup=confirm_delete_kb(habit_id),
    )
    await cb.answer()  # закрыть "часики" у callback


@router.callback_query(F.data.startswith("cancel_delete"))
async def cancel_delete(cb: CallbackQuery):
    await cb.message.edit_reply_markup(reply_markup=None)

    await cb.answer("↩️ Отменено", show_alert=False)


@router.callback_query(F.data.startswith("confirm_delete:"))
async def confirm_delete(cb: CallbackQuery, habit_client: HabitServiceClient):
    habit_id = int(cb.data.split(":")[1])

    try:
        await habit_client.delete_habit(habit_id)

        # UX: убираем кнопки подтверждения и показываем короткое подтверждение
        await cb.message.edit_reply_markup(reply_markup=None)
        await cb.answer("🗑️ Привычка удалена", show_alert=False)

        # Дополнительно (по желанию): можно отправить сообщение в чат.
        # await cb.message.answer("🗑️ Привычка удалена.")

    except BackendError as e:
        await reply_error(cb, format_backend_error(e))


@router.callback_query(lambda c: c.data.startswith("edit_name"))
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    habit_id = int(callback.data.split(":")[1])  # type: ignore
    await state.update_data(habit_id=habit_id)
    await callback.message.answer("Введите новое имя для привычки:")
    await state.set_state(EditHabit.waiting_for_name)


@router.message(EditHabit.waiting_for_name)
async def process_new_name(message: Message, state: FSMContext, habit_client: HabitServiceClient):
    data = await state.get_data()
    habit_id = data["habit_id"]
    new_name = message.text
    try:
        await habit_client.edit_habit(habit_id, {"name": new_name})

        await message.answer("Имя привычки обновлено!")
        await state.clear()
    except BackendError as e:
        await reply_error(message, format_backend_error(e))


@router.callback_query(lambda c: c.data.startswith("edit_desc"))
async def edit_desc_start(callback: CallbackQuery, state: FSMContext):
    habit_id = int(callback.data.split(":")[1])  # type: ignore
    await state.update_data(habit_id=habit_id)

    await callback.message.answer("Введите новое описание:")  # type: ignore
    await state.set_state(EditHabit.waiting_for_description)


@router.message(EditHabit.waiting_for_description)
async def process_new_description(message: Message, state: FSMContext, habit_client: HabitServiceClient):
    data = await state.get_data()
    habit_id = data["habit_id"]
    new_desc = message.text
    try:
        await habit_client.edit_habit(habit_id, {"description": new_desc})

        await message.answer("Описание обновлено!")
        await state.clear()
    except BackendError as e:
        await reply_error(message, format_backend_error(e))
