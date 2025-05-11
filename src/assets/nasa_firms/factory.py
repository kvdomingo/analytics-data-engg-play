from textwrap import dedent

import dagster as dg
import polars as pl
import polars_st as st
from dagster_duckdb import DuckDBResource

from src.dbt_project import dbt_project
from src.lib.core import (
    emit_standard_df_metadata,
    get_multi_partition_keys_from_context,
    init_duckdb,
)
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
        metadata={
            "schema": dbt_project.name,
            "partition_expr": {
                "date": "acq_date",
                "country": "country_id",
            },
        },
        partitions_def=country_daily_partitions_def,
    )
    async def extract_raw(
        context: dg.AssetExecutionContext, nasa_firms_api: NasaFirmsApi
    ) -> pl.DataFrame:
        partition_keys = get_multi_partition_keys_from_context(context)
        country = partition_keys["country"]
        date = partition_keys["date"]

        csv = await nasa_firms_api.get_bytes(country, date, satellite_code)
        df = pl.read_csv(csv, infer_schema=False)
        context.add_output_metadata(emit_standard_df_metadata(df))
        return df

    return dg.Definitions(
        assets=[extract_raw],
        resources=RESOURCES,
    )


UPSTREAM_KEYS = [
    "nasa_firms__viirs_silver",
    "nasa_firms__viirs",
]


def build_viirs_delta_asset(upstream_asset_key: str):
    @dg.asset(
        name=f"{upstream_asset_key}_delta",
        group_name="nasa_firms",
        io_manager_key=IOManager.DELTALAKE.value,
        kinds={"polars", "deltalake", "googlecloud"},
        partitions_def=country_daily_partitions_def,
        metadata={
            "partition_by": ["country_id", "date"],
        },
        deps=[upstream_asset_key],
    )
    def output_delta(
        context: dg.AssetExecutionContext,
        duckdb: DuckDBResource,
    ) -> pl.DataFrame:
        partition_keys = get_multi_partition_keys_from_context(context)

        with duckdb.get_connection() as conn:
            init_duckdb(conn)
            df = (
                conn.sql(
                    dedent(f"""
                    SELECT
                        id,
                        country_id,
                        ST_AsText(geometry) AS geometry,
                        "date",
                        "timestamp",
                        bright_ti4,
                        bright_ti5,
                        scan,
                        track,
                        satellite,
                        instrument,
                        confidence,
                        version,
                        frp,
                        daynight
                    FROM {dbt_project.name}.{upstream_asset_key}
                    WHERE
                       timestamp::DATE = $date::DATE
                       AND country_id = $country
                    """),
                    params={
                        "date": partition_keys["date"],
                        "country": partition_keys["country"],
                    },
                )
                .pl()
                .with_columns(geometry=st.from_wkt("geometry"))
            )

        context.add_output_metadata(emit_standard_df_metadata(df.st.to_wkt()))
        return df

    return dg.Definitions(
        assets=[output_delta],
        resources=RESOURCES,
    )
