from datetime import datetime
from zoneinfo import ZoneInfo

import dagster as dg
import polars as pl
from curl_cffi import AsyncSession

from src.dbt_project import dbt_project
from src.resources import IOManager


@dg.asset(
    group_name="gpu_tracker",
    kinds={"polars", "duckdb"},
    io_manager_key=IOManager.DUCKDB.value,
    metadata={"schema": dbt_project.name},
)
async def gpu_tracker__dynaquest_raw(context: dg.AssetExecutionContext):
    category = "graphics-card"

    async with AsyncSession(
        base_url="https://dynaquestpc.com", allow_redirects=True, impersonate="chrome"
    ) as session:
        # Access Shopify products.json directly
        res = await session.get(
            f"/collections/{category}/products.json",
            params={
                "sort_by": "best-selling",
                "page": 1,
                "limit": 1000,
            },
        )
        data = res.json()

    if data.get("products") is None:
        raise ValueError("No products found")

    products = data["products"]
    df = pl.from_dicts(products).with_columns(
        retrieved_at=pl.lit(datetime.now(ZoneInfo("UTC"))),
    )
    context.add_output_metadata({"dagster/row_count": len(df)})
    return df
