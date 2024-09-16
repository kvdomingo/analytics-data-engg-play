import polars as pl
from dagster import AssetExecutionContext, asset
from dagster_dbt import DbtCliResource, dbt_assets
from dagster_duckdb import DuckDBResource
from duckdb.duckdb import DuckDBPyConnection

from src.dbt_project import dbt_project
from src.resources import IOManager
from src.settings import settings


@asset(
    compute_kind="duckdb",
    io_manager_key=IOManager.DUCKDB.value,
    metadata={"schema": "ae_de_play"},
)
def raw_afg(context: AssetExecutionContext, duckdb: DuckDBResource) -> pl.DataFrame:
    with duckdb.get_connection() as conn:
        conn: DuckDBPyConnection
        df = conn.execute(
            f"""
            SELECT *
            FROM read_csv(
                '{str(settings.BASE_DIR / "data/src/master/AFG_school_geolocation_coverage_master.csv")}',
                all_varchar = true
            )
            """,
        ).pl()

    context.add_output_metadata({"row_count": len(df)})
    return df


@dbt_assets(manifest=dbt_project.manifest_path)
def afg_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
