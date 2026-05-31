from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)

    bankable_data_root: str | None = Field(
        default=None,
        validation_alias=AliasChoices("ATTESTRWA_DATA_ROOT", "BANKABLE_DATA_ROOT"),
    )
    bankable_cors_origins: str = Field(
        default="",
        validation_alias=AliasChoices("ATTESTRWA_CORS_ORIGINS", "BANKABLE_CORS_ORIGINS"),
    )
    bankable_api_version: str = Field(
        default="1.0.0",
        validation_alias=AliasChoices("ATTESTRWA_API_VERSION", "BANKABLE_API_VERSION"),
    )
    bankable_log_level: str = Field(
        default="INFO",
        validation_alias=AliasChoices("ATTESTRWA_LOG_LEVEL", "BANKABLE_LOG_LEVEL"),
    )
    bankable_ai_tier: str = Field(
        default="demo_local",
        validation_alias=AliasChoices("ATTESTRWA_AI_TIER", "BANKABLE_AI_TIER"),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
