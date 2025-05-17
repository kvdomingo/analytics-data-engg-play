import json

import dagster as dg
from dagster_dbt import (
    DbtCliResource,
    dbt_assets as assets,
)

from src.dbt_project import dbt_project
from src.partitions import country_daily_partitions_def, ph_region_batch_partitions_def


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
    partition_keys: dg.MultiPartitionKey = context.partition_key
    partition_keys_dims = partition_keys.keys_by_dimension
    country = partition_keys_dims["country"]
    date = partition_keys_dims["date"]

    yield from (
        dbt.cli(
            [
                "build",
                "--vars",
                json.dumps({"date": date, "country": country}),
            ],
            context=context,
        )
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )


@assets(
    manifest=dbt_project.manifest_path,
    select=f"fqn:{dbt_project.name}.ph_mte25.*",
    partitions_def=ph_region_batch_partitions_def,
)
def ph_mte25__dbt_assets(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    partition_keys: dg.MultiPartitionKey = context.partition_key
    partition_keys_dims = partition_keys.keys_by_dimension
    region = partition_keys_dims["region"]
    batch = partition_keys_dims["batch"]

    yield from (
        dbt.cli(
            [
                "build",
                "--vars",
                json.dumps({"region": region, "batch": batch}),
            ],
            context=context,
        )
        .stream()
        .fetch_row_counts()
        .fetch_column_metadata()
    )
