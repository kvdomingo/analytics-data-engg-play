from enum import Enum

from dagster import EnvVar
from dagster_airbyte import AirbyteResource
from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

from src.settings import settings


class IOManager(Enum):
    DUCKDB = "duckdb_io_manager"


class Resource(Enum):
    DUCKDB = "duckdb"
    DBT = "dbt"
    AIRBYTE = "airbyte"


RESOURCES = {
    Resource.DUCKDB.value: DuckDBResource(database=settings.DUCKDB_DATABASE),
    Resource.DBT.value: DbtCliResource(project_dir=settings.BASE_DIR),
    Resource.AIRBYTE.value: AirbyteResource(
        host=settings.AIRBYTE_HOST,
        port=str(settings.AIRBYTE_PORT),
        username=EnvVar("AIRBYTE_USERNAME"),
        password=EnvVar("AIRBYTE_PASSWORD"),
    ),
    IOManager.DUCKDB.value: DuckDBPolarsIOManager(database=settings.DUCKDB_DATABASE),
}
