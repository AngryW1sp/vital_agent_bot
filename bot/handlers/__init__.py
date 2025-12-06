from .start import router as start_router
from .habits.habits import router as habit_router

all_routers = [
    start_router,
    habit_router,
]
