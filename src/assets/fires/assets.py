import io

import dagster as dg
import polars as pl
from dagster import MetadataValue
from httpx import AsyncClient

from src.partitions import daily_partitions_def
from src.resources import IOManager
from src.settings import settings


@dg.asset(
    partitions_def=daily_partitions_def,
    io_manager_key=IOManager.S3.value,
    kinds={"s3"},
)
async def fires__raw(context: dg.AssetExecutionContext) -> str:
    async with AsyncClient(base_url=settings.NASA_FIRMS_BASE_URL) as client:
        res = await client.get(
            f"/api/country/csv/{settings.NASA_FIRMS_MAP_KEY}/VIIRS_SNPP_NRT/PHL/1/{context.partition_key}"
        )
        res.raise_for_status()
        text = res.text

    context.add_output_metadata({"size": MetadataValue.int(len(text))})
    return text


@dg.asset(
    partitions_def=daily_partitions_def,
    io_manager_key=IOManager.DELTALAKE.value,
    metadata={
        "partition_expr": "measurement_date",
    },
    kinds={"s3", "polars", "deltalake"},
)
def fires__raw_delta(
    context: dg.AssetExecutionContext,
    fires__raw: str,
) -> pl.DataFrame:
    with io.StringIO(fires__raw) as buf:
        df = pl.read_csv(buf)

    df = df.with_columns(measurement_date=pl.lit(context.partition_key).cast(pl.Date()))
    return df
