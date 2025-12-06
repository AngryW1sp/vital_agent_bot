from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.habits.habit_kb import get_habit_complete_kb
from bot.services.requests import habit_client
from bot.utils.progress import render_progress


router = Router()


@router.message(F.text == 'Список привычек')
async def get_my_habits(message: Message):
    request = await habit_client.get_habits()
    for result in filter(lambda x: x['is_active'] == True, request):
        name = result['name']
        description = result['description']
        text = (
            f'<strong>{name}</strong>\n\n'
            f'<em>{description}</em>\n\n'
            f'{render_progress(result['completed_days_count'])}'
        )

        await message.answer(text=text, reply_markup=get_habit_complete_kb(result['id']))
