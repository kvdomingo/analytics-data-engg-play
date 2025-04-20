import dagster as dg
import polars as pl
from dagster_aws.s3 import S3Resource

from src.internal.core import (
    cast_schema_types,
    emit_standard_df_metadata,
    get_csv_from_s3_datasets,
)
from src.resources import IOManager
from src.schemas.climate_air_quality import ClimateAirQuality


@dg.asset(kinds={"s3", "polars"})
def caq__extract(context: dg.AssetExecutionContext, s3: S3Resource) -> pl.DataFrame:
    csv = get_csv_from_s3_datasets(path="project-cchain/climate_air_quality.csv", s3=s3)
    df = pl.read_csv(csv)
    context.add_output_metadata(emit_standard_df_metadata(df))
    return df


@dg.asset(kinds={"polars"})
def caq__transform(
    context: dg.AssetExecutionContext,
    caq__extract: pl.DataFrame,
) -> pl.DataFrame:
    df = cast_schema_types(caq__extract, ClimateAirQuality)
    context.add_output_metadata(emit_standard_df_metadata(df))
    return df


@dg.asset(kinds={"polars", "duckdb"}, io_manager_key=IOManager.DUCKDB.value)
def climate_air_quality(
    context: dg.AssetExecutionContext,
    caq__transform: pl.DataFrame,
) -> pl.DataFrame:
    df = caq__transform
    context.add_output_metadata(emit_standard_df_metadata(df))
    return df
