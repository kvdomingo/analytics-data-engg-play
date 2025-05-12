import dagster as dg
import polars as pl
from dagster_aws.s3 import S3Resource
from dagster_duckdb import DuckDBResource

from src.dbt_project import dbt_project
from src.lib.core import (
    emit_standard_df_metadata,
    get_csv_from_s3_datasets,
)
from src.resources import RESOURCES, IOManager

CCHAIN_DATASETS = [
    "climate_atmosphere",
    "disease_lgu_disaggregated_totals",
    "disease_pidsr_totals",
    "location",
    "mapbox_health_facility_brgy_isochrones",
]


def build_cchain_raw_asset(filename: str):
    @dg.asset(
        name=f"cchain__{filename}_raw",
        group_name="cchain",
        kinds={"s3", "polars", "duckdb"},
        io_manager_key=IOManager.DUCKDB.value,
        metadata={"schema": dbt_project.name},
    )
    def extract_raw(context: dg.AssetExecutionContext, s3: S3Resource) -> pl.DataFrame:
        datasets_path_prefix = "project-cchain"
        csv = get_csv_from_s3_datasets(
            path=f"{datasets_path_prefix}/{filename}.csv", s3=s3
        )
        df = pl.read_csv(csv, infer_schema=False)
        context.add_output_metadata(emit_standard_df_metadata(df))
        return df

    return dg.Definitions(
        assets=[extract_raw],
        resources=RESOURCES,
    )


UPSTREAM_KEYS = [
    "cchain__disease_climate",
]


def build_cchain_delta_asset(upstream_asset_key: str):
    @dg.asset(
        name=f"{upstream_asset_key}_delta",
        group_name="cchain",
        io_manager_key=IOManager.DELTALAKE.value,
        kinds={"polars", "deltalake", "googlecloud"},
        deps=[upstream_asset_key],
        pool="deltalake",
    )
    def output_delta(
        context: dg.AssetExecutionContext,
        duckdb: DuckDBResource,
    ) -> pl.DataFrame:
        with duckdb.get_connection() as conn:
            df = conn.table(f"{dbt_project.name}.{upstream_asset_key}").pl()

        context.add_output_metadata(emit_standard_df_metadata(df))
        return df

    return dg.Definitions(
        assets=[output_delta],
        resources=RESOURCES,
    )
