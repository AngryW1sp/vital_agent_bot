from aiogram.filters.callback_data import CallbackData


class HabitCallback(CallbackData, prefix='habbit'):
    id: int
