from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Support System"
    app_env: str = "development"
    app_version: str = "0.1.0"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    database_url: str

    groq_api_key: str = Field(
        min_length=1,
        repr=False,
    )
    groq_model: str = "llama-3.3-70b-versatile"
    groq_base_url: str = (
        "https://api.groq.com/openai/v1"
    )

    llm_timeout_seconds: float = 60.0
    llm_max_output_tokens: int = 500

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()