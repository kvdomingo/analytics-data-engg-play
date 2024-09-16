from enum import Enum

from dagster_dbt import DbtCliResource
from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

from src.settings import settings


class IOManager(Enum):
    DUCKDB = "duckdb_io_manager"


class Resource(Enum):
    DUCKDB = "duckdb"
    DBT = "dbt"


RESOURCES = {
    Resource.DUCKDB.value: DuckDBResource(database=settings.DUCKDB_DATABASE),
    Resource.DBT.value: DbtCliResource(project_dir=settings.BASE_DIR),
    IOManager.DUCKDB.value: DuckDBPolarsIOManager(database=settings.DUCKDB_DATABASE),
}
