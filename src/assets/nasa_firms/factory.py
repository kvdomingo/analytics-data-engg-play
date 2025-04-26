import dagster as dg
import polars as pl

from src.dbt_project import dbt_project
from src.internal.core import emit_standard_df_metadata
from src.partitions import country_daily_partitions_def
from src.resources import RESOURCES, IOManager
from src.resources.nasa_firms_api import NasaFirmsApi

SATELLITE_CODES = ["SNPP", "NOAA20", "NOAA21"]


def build_viirs_raw_asset(satellite_code: str):
    @dg.asset(
        name=f"nasa_firms__viirs_{satellite_code.lower()}_raw",
        group_name="nasa_firms",
        kinds={"polars", "duckdb"},
        io_manager_key=IOManager.DUCKDB.value,
        metadata={"schema": dbt_project.name},
        partitions_def=country_daily_partitions_def,
    )
    async def extract_raw(
        context: dg.AssetExecutionContext, nasa_firms_api: NasaFirmsApi
    ) -> pl.DataFrame:
        partition_keys: dg.MultiPartitionKey = context.partition_key
        partition_keys_dims = partition_keys.keys_by_dimension
        country = partition_keys_dims["country"]
        date = partition_keys_dims["date"]

        text = await nasa_firms_api.get_text(country, date, satellite_code)
        df = pl.read_csv(text, infer_schema=False)
        context.add_output_metadata(emit_standard_df_metadata(df))
        return df

    return dg.Definitions(
        assets=[extract_raw],
        resources=RESOURCES,
    )
