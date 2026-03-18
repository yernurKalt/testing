from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

db_link = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"