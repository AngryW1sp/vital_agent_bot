from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Список привычек')]
    ], resize_keyboard=True)
    return kb
