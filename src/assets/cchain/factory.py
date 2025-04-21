import dagster as dg
import polars as pl
from dagster_aws.s3 import S3Resource

from src.internal.core import (
    emit_standard_df_metadata,
    get_csv_from_s3_datasets,
    schema_transforms,
)
from src.resources import RESOURCES, IOManager
from src.schemas.climate_air_quality import ClimateAirQuality
from src.schemas.climate_atmosphere import ClimateAtmosphere
from src.schemas.disease_pidsr_totals import DiseasePidsrTotals
from src.schemas.location import Location

CCHAIN_DATASETS = [
    ("climate_air_quality", ClimateAirQuality),
    ("climate_atmosphere", ClimateAtmosphere),
    ("disease_pidsr_totals", DiseasePidsrTotals),
    ("location", Location),
]


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
        df = schema_transforms(df, schema)
        context.add_output_metadata(emit_standard_df_metadata(df))
        return df

    return dg.Definitions(
        assets=[etl],
        resources=RESOURCES,
    )
