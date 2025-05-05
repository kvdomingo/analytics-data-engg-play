from enum import Enum

from dagster_aws.s3 import S3PickleIOManager, S3Resource
from dagster_dbt import DbtCliResource
from dagster_deltalake import LocalConfig
from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

from src.settings import settings

from .io_managers.deltalake import DeltaLakePolarsIOManager
from .nasa_firms_api import NasaFirmsApi


class IOManager(Enum):
    DUCKDB = "duckdb_io_manager"
    DELTALAKE = "deltalake_io_manager"
    S3 = "s3_io_manager"


class Resource(Enum):
    DUCKDB = "duckdb"
    DBT = "dbt"
    S3 = "s3"
    NASA_FIRMS_API = "nasa_firms_api"


_s3_resource = S3Resource(
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    region_name=settings.MINIO_REGION,
)


RESOURCES = {
    Resource.DUCKDB.value: DuckDBResource(database=settings.DUCKDB_DATABASE),
    Resource.DBT.value: DbtCliResource(project_dir=settings.BASE_DIR),
    Resource.S3.value: _s3_resource,
    Resource.NASA_FIRMS_API.value: NasaFirmsApi(map_key=settings.NASA_FIRMS_MAP_KEY),
    IOManager.DUCKDB.value: DuckDBPolarsIOManager(database=settings.DUCKDB_DATABASE),
    IOManager.DELTALAKE.value: DeltaLakePolarsIOManager(
        path_prefix=[*settings.BASE_DIR.parts, "data", "lake"],
        table_config={
            "delta.enableChangeDataFeed": "true",
            "delta.logRetentionDuration": "interval 1000000000 weeks",
        },
        storage_config=LocalConfig(),
    ),
    IOManager.S3.value: S3PickleIOManager(
        s3_resource=_s3_resource,
        s3_bucket=settings.MINIO_BUCKET,
        s3_prefix="dagster-io",
    ),
}
