from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHON_ENV: Literal["development", "production"] = "production"
    BASE_DIR: Path = Path(__file__).parent.parent
    DEFAULT_TZ: str = "Asia/Manila"

    NASA_FIRMS_MAP_KEY: str
    NASA_FIRMS_BASE_URL: str = "https://firms.modaps.eosdis.nasa.gov"

    MINIO_ENDPOINT: str
    MINIO_REGION: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str

    GCS_BUCKET: str
    GCS_APPLICATION_CREDENTIALS: str

    @computed_field
    @property
    def IS_PRODUCTION(self) -> bool:
        return self.PYTHON_ENV == "production"

    @computed_field
    @property
    def DUCKDB_DATABASE(self) -> str:
        return str(self.BASE_DIR / "data/lake/db.duckdb")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
