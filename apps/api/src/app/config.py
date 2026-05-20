from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bankable_data_root: str | None = None
    bankable_cors_origins: str = ""
    bankable_api_version: str = "0.5.13"
    bankable_log_level: str = "INFO"
    bankable_ai_tier: str = "demo_local"


@lru_cache
def get_settings() -> Settings:
    return Settings()
