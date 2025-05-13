from datetime import datetime
from json import JSONDecodeError
from typing import Literal
from zoneinfo import ZoneInfo

import dagster as dg
import polars as pl

from src.dbt_project import dbt_project
from src.lib.core import (
    emit_standard_df_metadata,
    get_multi_partition_keys_from_context,
)
from src.partitions import ph_region_batch_partitions_def
from src.resources import RESOURCES, IOManager
from src.resources.gma_api import GmaApi


def build_ph_mte25_raw_asset(category: Literal["senator", "party"]):
    @dg.asset(
        name=f"ph_mte25__{category}_raw",
        group_name="ph_mte25",
        kinds={"polars", "duckdb"},
        io_manager_key=IOManager.DUCKDB.value,
        metadata={
            "schema": dbt_project.name,
            "partition_expr": {
                "region": "region",
                "batch": "batch",
            },
        },
        partitions_def=ph_region_batch_partitions_def,
    )
    async def extract_raw(
        context: dg.AssetExecutionContext, gma_data_api: GmaApi
    ) -> pl.DataFrame:
        partition_keys = get_multi_partition_keys_from_context(context)
        region_str = partition_keys["region"]
        batch = partition_keys["batch"]

        region = region_str.replace(" ", "_").upper()

        async with gma_data_api.get_async_client() as client:
            res = await client.get(f"/batch/{batch}/{region}.json")
            res.raise_for_status()

            try:
                data = res.json()
            except JSONDecodeError:
                context.log.error(f"Invalid JSON:\n{res.text}")
                raise

        results = data.get("result")
        cat = next(r for r in results if category in r.get("contest", "").lower())
        candidates = cat.get("candidates")
        as_of = data.get("result_as_of")
        df = pl.from_dicts(candidates).with_columns(
            region=pl.lit(region_str),
            batch=pl.lit(int(batch)),
            timestamp=pl.lit(
                datetime.strptime(as_of, "%Y/%m/%d %H:%M:%S").replace(
                    tzinfo=ZoneInfo("Asia/Manila")
                )
            ),
        )
        context.add_output_metadata(emit_standard_df_metadata(df))
        return df

    return dg.Definitions(
        assets=[extract_raw],
        resources=RESOURCES,
    )
