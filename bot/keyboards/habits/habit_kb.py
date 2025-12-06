from aiogram.types import InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup


def get_habit_complete_kb(habit_id: int):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Выполнить ✅',
                              callback_data=f'{habit_id}:habit')]
    ])
    return kb
