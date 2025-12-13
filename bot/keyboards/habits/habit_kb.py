from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def get_habits_kb(habit_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="✏️ Изменить имя", callback_data=f"edit_name:{habit_id}")
    kb.button(text="📝 Изменить описание",
              callback_data=f"edit_desc:{habit_id}")
    kb.button(text="🗑️ Удалить привычку",
              callback_data=f"habit_delete:{habit_id}")

    kb.adjust(1, 1, 1)
    return kb.as_markup()


def get_start_habit():
    kb = ReplyKeyboardBuilder()

    kb.button(text="✅ Сегодня")
    kb.button(text="➕ Создать привычку")
    kb.button(text="📋 Все привычки")
    kb.button(text="⬅️ В главное меню")

    kb.adjust(2, 1, 1)
    return kb.as_markup(resize_keyboard=True)


def complete_kb(habit_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="✅ Отметить выполненной сегодня",
        callback_data=f"complete_habit:{habit_id}",
    )
    kb.adjust(1)
    return kb.as_markup()


def confirm_delete_kb(habit_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="🗑️ Да, удалить",
              callback_data=f"confirm_delete:{habit_id}")
    kb.button(text="↩️ Отмена", callback_data="cancel_delete")
    kb.adjust(1, 1)
    return kb.as_markup()
