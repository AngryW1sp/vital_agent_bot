from pydantic_settings import SettingsConfigDict, BaseSettings
import logging

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    BACKEND_URL: str = "http://localhost:8000/api/v1/"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite+aiosqlite:///./bot.db"
    habit_service_url: str = "http://localhost:8000/api/v1"
    user_service_url: str = "http://localhost:8001/internal/users"
    internal_token: str = "your_internal_token"


settings = Settings()
