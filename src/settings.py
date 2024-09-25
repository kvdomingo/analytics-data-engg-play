from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent

    AIRBYTE_HOST: str
    AIRBYTE_PORT: int
    AIRBYTE_USERNAME: str
    AIRBYTE_PASSWORD: str

    @computed_field
    @property
    def DUCKDB_DATABASE(self) -> str:
        return str(self.BASE_DIR / "data/lake/duck.db")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
