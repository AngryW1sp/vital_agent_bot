from datetime import datetime, timezone
from bot.repository.teleuser import TokenRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def get_valid_token(session: AsyncSession, telegram_user_id: int):
    repo = TokenRepository(session)
    tele_user = await repo.get_by_telegram_user_id(telegram_user_id)
    if (
        tele_user
        and tele_user.expires_at
        and tele_user.expires_at > datetime.now(timezone.utc)
    ):
        return tele_user.acess_token
    return None
