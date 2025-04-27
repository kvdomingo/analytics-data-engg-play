import dagster as dg
from dagster_dbt import (
    DbtCliResource,
    dbt_assets as assets,
)

from src.dbt_project import dbt_project
from src.partitions import country_daily_partitions_def


@assets(manifest=dbt_project.manifest_path, select=f"fqn:{dbt_project.name}.cchain.*")
def cchain__dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from (
        dbt.cli(["build"], context=context)
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )


@assets(
    manifest=dbt_project.manifest_path,
    select=f"fqn:{dbt_project.name}.nasa_firms.*",
    partitions_def=country_daily_partitions_def,
)
def nasa_firms__dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from (
        dbt.cli(["build"], context=context)
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )
