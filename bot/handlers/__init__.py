from bot.handlers.start import router as start_router
from bot.handlers.habits.create_habit import router as habit_create_router
from bot.handlers.habits.habit_list import router as habit_list_router
from bot.handlers.habits.habits import router as habit_router
from bot.handlers.habits.today_habit import router as today_habit_list_router


all_routers = [
    start_router,
    habit_create_router,
    habit_list_router,
    habit_router,
    today_habit_list_router
]
