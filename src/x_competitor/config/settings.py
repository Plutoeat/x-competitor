from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    openai_api_key: str = ""
    openai_api_base: str = ""
    openai_model_name: str = "gpt-4o"

    # Search engine (Serper)
    serper_api_key: str = ""

    # Search engine (Tavily) — alternative
    tavily_api_key: str = ""

    # Output
    output_dir: Path = PROJECT_ROOT / "output"

    # Cache
    cache_dir: Path = PROJECT_ROOT / ".cache"
    cache_ttl_hours: int = 24


settings = Settings()