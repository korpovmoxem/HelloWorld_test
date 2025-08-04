from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SUPERHERO_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )


    def get_superhero_api_url(self) -> str:
        return f'https://superheroapi.com/api/{self.SUPERHERO_API_KEY}'


settings = Settings()