from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    groq_api_key: str
    database_url: str
    news_api_key: str = ""
    brave_api_key: str = ""
    frontend_url: str = "http://localhost:5173"
    environment: str = "development"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
