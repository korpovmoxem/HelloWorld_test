from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPERHERO_API_KEY: str
    DB_NAME: str
    DB_URL: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        extra='ignore'
    )


    def get_superhero_api_url(self) -> str:
        return f'https://superheroapi.com/api/{self.SUPERHERO_API_KEY}'


    def get_database_url(self) -> str:
        return f'postgresql+asyncpg:///./{self.DB_NAME}'


settings = Settings()