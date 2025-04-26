import dagster as dg
from dagster_dbt import (
    DbtCliResource,
    dbt_assets as assets,
)

from src.dbt_project import dbt_project


@assets(manifest=dbt_project.manifest_path)
def dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from (
        dbt.cli(["build"], context=context)
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )
