from datetime import datetime

from bot.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, func, BigInteger, Text


class TeleUser(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_user_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False
    )
    acess_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
