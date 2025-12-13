from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.start import get_start_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я твой личный помощник.\n\n"
        "📈 Я помогу тебе создавать привычки, отмечать выполнение и следить за прогрессом.\n\n"
        "Нажми кнопку ниже, чтобы начать ⬇️",
        reply_markup=get_start_menu(),
    )


@router.message(F.text == "⬅️ В главное меню")
async def back_to_main_menu(message: Message):
    await message.answer(
        "🏠 <strong>Главное меню</strong>\n\nВыберите раздел ⬇️",
        reply_markup=get_start_menu(),
    )
