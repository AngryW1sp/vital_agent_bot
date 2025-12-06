from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = ''

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
    )


settings = Settings()
