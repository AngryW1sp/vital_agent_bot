from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_menu():
    kb = ReplyKeyboardBuilder()
    kb.button(text="📈 Трекер привычек")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
