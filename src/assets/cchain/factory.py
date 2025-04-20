import dagster as dg
import polars as pl
from dagster_aws.s3 import S3Resource

from src.internal.core import (
    cast_schema_types,
    emit_standard_df_metadata,
    get_csv_from_s3_datasets,
)
from src.resources import RESOURCES, IOManager


def build_cchain_job(filename: str, schema: pl.Struct):
    @dg.asset(
        name=f"cchain__{filename}",
        group_name="cchain",
        kinds={"s3", "polars", "duckdb"},
        io_manager_key=IOManager.DUCKDB.value,
    )
    def etl(context: dg.AssetExecutionContext, s3: S3Resource) -> pl.DataFrame:
        csv = get_csv_from_s3_datasets(path=f"project-cchain/{filename}.csv", s3=s3)
        df = pl.read_csv(csv)
        df = cast_schema_types(df, schema)
        context.add_output_metadata(emit_standard_df_metadata(df))
        return df

    return dg.Definitions(
        assets=[etl],
        resources=RESOURCES,
    )
