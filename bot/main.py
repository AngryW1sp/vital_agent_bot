import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.core.config import settings
from bot.handlers import all_routers
from bot.services.requests import HabitServiceClient


async def main():
    bot = Bot(token=settings.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    for router in all_routers:
        dp.include_router(router)
    habit_client = HabitServiceClient(settings.BACKEND_URL)
    dp["habit_client"] = habit_client

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        await dp.start_polling(bot)
    finally:
        await habit_client.client.aclose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершил свою работу!')
