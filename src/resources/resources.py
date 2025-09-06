from enum import Enum

from dagster_aws.s3 import S3PickleIOManager, S3Resource
from dagster_dbt import DbtCliResource
from dagster_deltalake import GcsConfig
from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

from src.settings import settings

from .gma_api import GmaApi
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
    GMA_DATA_API = "gma_data_api"
    GMA_METADATA_API = "gma_metadata_api"


_s3_resource = S3Resource(
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY.get_secret_value(),
    aws_secret_access_key=settings.MINIO_SECRET_KEY.get_secret_value(),
    region_name=settings.MINIO_REGION,
)


RESOURCES = {
    Resource.DUCKDB.value: DuckDBResource(database=settings.DUCKDB_DATABASE),
    Resource.DBT.value: DbtCliResource(project_dir=settings.BASE_DIR),
    Resource.S3.value: _s3_resource,
    Resource.NASA_FIRMS_API.value: NasaFirmsApi(
        map_key=settings.NASA_FIRMS_MAP_KEY.get_secret_value()
    ),
    Resource.GMA_METADATA_API.value: GmaApi(base_url="https://e25d-cf.gmanetwork.com"),
    Resource.GMA_DATA_API.value: GmaApi(base_url="https://e25vh-cf.gmanetwork.com"),
    IOManager.DUCKDB.value: DuckDBPolarsIOManager(
        database=settings.DUCKDB_DATABASE,
        connection_config={
            "autoinstall_known_extensions": "true",
            "autoload_known_extensions": "true",
        },
    ),
    IOManager.DELTALAKE.value: DeltaLakePolarsIOManager(
        path_prefix=[settings.GCS_BUCKET.get_secret_value()],
        table_config={
            "delta.enableChangeDataFeed": "true",
            "delta.logRetentionDuration": "interval 1000000000 weeks",
        },
        storage_config=GcsConfig(
            provider="gcs",
            bucket=settings.GCS_BUCKET.get_secret_value(),
            application_credentials=settings.GCS_APPLICATION_CREDENTIALS.get_secret_value(),
        ),
    ),
    IOManager.S3.value: S3PickleIOManager(
        s3_resource=_s3_resource,
        s3_bucket=settings.MINIO_BUCKET,
        s3_prefix="dagster-io",
    ),
}
