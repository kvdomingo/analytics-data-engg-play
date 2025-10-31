from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PYTHON_ENV: Literal["development", "production"] = "production"
    BASE_DIR: Path = Path(__file__).parent.parent
    DEFAULT_TZ: str = "Asia/Manila"

    NASA_FIRMS_MAP_KEY: SecretStr
    NASA_FIRMS_BASE_URL: str = "https://firms.modaps.eosdis.nasa.gov"

    MINIO_ENDPOINT: str
    MINIO_REGION: str
    MINIO_ACCESS_KEY: SecretStr
    MINIO_SECRET_KEY: SecretStr
    MINIO_BUCKET: str

    GCS_BUCKET: SecretStr
    GCS_APPLICATION_CREDENTIALS: SecretStr

    RAPIDAPI_INSTAGRAM_API_KEY: SecretStr

    GPU_TRACKER_POSTGRES_DATABASE: str
    GPU_TRACKER_POSTGRES_USERNAME: SecretStr
    GPU_TRACKER_POSTGRES_PASSWORD: SecretStr
    GPU_TRACKER_POSTGRES_HOST: str
    GPU_TRACKER_POSTGRES_PORT: int

    @computed_field
    @property
    def IS_PRODUCTION(self) -> bool:
        return self.PYTHON_ENV == "production"

    @computed_field
    @property
    def DUCKDB_DATABASE(self) -> str:
        return str(self.BASE_DIR / "data/lake/db.duckdb")

    @computed_field
    @property
    def GPU_TRACKER_POSTGRES_URL(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.GPU_TRACKER_POSTGRES_USERNAME.get_secret_value(),
                password=self.GPU_TRACKER_POSTGRES_PASSWORD.get_secret_value(),
                host=self.GPU_TRACKER_POSTGRES_HOST,
                port=self.GPU_TRACKER_POSTGRES_PORT,
                path=self.GPU_TRACKER_POSTGRES_DATABASE,
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
