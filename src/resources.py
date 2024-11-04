from enum import Enum

from dagster_aws.s3 import S3PickleIOManager, S3Resource
from dagster_dbt import DbtCliResource
from dagster_deltalake import S3Config, WriteMode
from dagster_deltalake.config import ClientConfig
from dagster_deltalake_polars import DeltaLakePolarsIOManager
from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

from src.settings import settings


class IOManager(Enum):
    DUCKDB = "duckdb_io_manager"
    DELTALAKE = "deltalake_io_manager"
    S3 = "s3_io_manager"


class Resource(Enum):
    DUCKDB = "duckdb"
    DBT = "dbt"
    S3 = "s3"


_s3_resource = S3Resource(
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
)


RESOURCES = {
    Resource.DUCKDB.value: DuckDBResource(database=settings.DUCKDB_DATABASE),
    Resource.DBT.value: DbtCliResource(project_dir=settings.BASE_DIR),
    Resource.S3.value: _s3_resource,
    IOManager.DUCKDB.value: DuckDBPolarsIOManager(database=settings.DUCKDB_DATABASE),
    IOManager.DELTALAKE.value: DeltaLakePolarsIOManager(
        root_uri=f"s3a://{settings.MINIO_BUCKET}",
        mode=WriteMode.append,
        storage_options=S3Config(
            endpoint=settings.MINIO_ENDPOINT,
            access_key_id=settings.MINIO_ACCESS_KEY,
            secret_access_key=settings.MINIO_SECRET_KEY,
            bucket=settings.MINIO_BUCKET,
            allow_unsafe_rename=True,
        ),
        client_options=ClientConfig(allow_http=True),
    ),
    IOManager.S3.value: S3PickleIOManager(
        s3_resource=_s3_resource,
        s3_bucket=settings.MINIO_BUCKET,
        s3_prefix="dagster-io",
    ),
}
