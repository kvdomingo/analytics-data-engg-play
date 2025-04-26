from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, computed_field
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

    DATA_DB_USERNAME: str
    DATA_DB_PASSWORD: str
    DATA_DB_DATABASE: str
    DATA_DB_HOST: str
    DATA_DB_PORT: int

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
    def DATA_DB_CONNECTION(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.DATA_DB_USERNAME,
                password=self.DATA_DB_PASSWORD,
                host=self.DATA_DB_HOST,
                port=self.DATA_DB_PORT,
                path=self.DATA_DB_DATABASE,
            )
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
