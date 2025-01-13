from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    user: str
    password: str
    db: str
    port: int = 5432


class Settings(BaseSettings):
    web_port: int = 8000
    is_debug: bool = False

    database: DatabaseSettings

    model_config: SettingsConfigDict = SettingsConfigDict(env_nested_delimiter="__")


@lru_cache
def get_settings() -> Settings:
    return Settings()
