from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.habits.habit_kb import get_start_habit
from bot.services.requests import HabitServiceClient
from bot.services.errors import BackendError, format_backend_error, reply_error
router = Router()


class HabitCreateForm(StatesGroup):
    name = State()
    description = State()


@router.message(F.text == '➕ Создать привычку')
async def create_habit(message: Message, state: FSMContext):
    await state.set_state(HabitCreateForm.name)
    await message.answer(
        "➕ <strong>Создаём привычку</strong>\n\n"
        "Введите название (5–200 символов):",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(HabitCreateForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(HabitCreateForm.description)
    await message.answer(
        "📝 Теперь добавьте описание (можно коротко).\n"
        "Если описания нет — отправьте «-»"
    )


@router.message(HabitCreateForm.description)
async def process_description(message: Message, state: FSMContext, habit_client: HabitServiceClient):
    desc = message.text
    if desc == "-":
        desc = None

    await state.update_data(description=desc)
    data = await state.get_data()
    await state.clear()

    try:
        created = await habit_client.create_habit(data)

        name = created.get("name", data.get("name", ""))
        description = created.get("description") or "Без описания"

        await message.answer(
            "✅ Привычка сохранена!\n\n"
            f"<strong>{name}</strong>\n"
            f"<em>{description}</em>\n\n"
            "Теперь можно отмечать выполнение в разделе «✅ Сегодня» 🔥",
            reply_markup=get_start_habit(),
        )
    except BackendError as e:
        await reply_error(message, format_backend_error(e))
        # UX: если ошибка — вернём меню, чтобы не “повисли”
        await message.answer("Выберите действие ⬇️", reply_markup=get_start_habit())
