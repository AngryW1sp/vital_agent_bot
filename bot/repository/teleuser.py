from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.models.tele_user import TeleUser


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_user_id(self, telegram_user_id: int):
        result = await self.session.execute(
            select(TeleUser).where(TeleUser.telegram_user_id == telegram_user_id)
        )
        return result.scalars().first()

    async def upsert(
        self, telegram_user_id: int, access_token: str, expires_at: datetime
    ):
        tele_user = await self.get_by_telegram_user_id(telegram_user_id)
        if tele_user:
            tele_user.acess_token = access_token
            tele_user.expires_at = expires_at
        else:
            tele_user = TeleUser(
                telegram_user_id=telegram_user_id,
                acess_token=access_token,
                expires_at=expires_at,
            )
            self.session.add(tele_user)
        await self.session.commit()
        return tele_user
