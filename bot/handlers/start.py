from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import httpx

from bot.keyboards.start import get_start_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Привет, я твой личный помощник!", reply_markup=get_start_menu()
    )
