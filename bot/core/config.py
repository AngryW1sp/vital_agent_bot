from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = ''
    BACKEND_URL: str = 'http://localhost:8000/api/v1/'
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()
