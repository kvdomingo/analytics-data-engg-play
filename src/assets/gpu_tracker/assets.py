import random
from asyncio import sleep
from datetime import datetime
from zoneinfo import ZoneInfo

import dagster as dg
import polars as pl
from aiofiles import open
from curl_cffi import AsyncSession

from src.dbt_project import dbt_project
from src.lib.gpu_tracker import crawl_shopify_products_json
from src.resources import IOManager
from src.settings import settings


@dg.asset(
    group_name="gpu_tracker",
    kinds={"polars", "duckdb"},
    io_manager_key=IOManager.DUCKDB.value,
    metadata={"schema": dbt_project.name},
)
async def gpu_tracker__dynaquest_raw(context: dg.AssetExecutionContext):
    products = await crawl_shopify_products_json(
        context,
        base_url="https://dynaquestpc.com",
        path="/collections/graphics-card/products.json",
        extra_params={
            "sort_by": "best-selling",
        },
    )

    df = pl.from_dicts(products).with_columns(
        retrieved_at=pl.lit(datetime.now(ZoneInfo("UTC"))),
    )
    context.add_output_metadata({"dagster/row_count": len(df)})
    return df


@dg.asset(
    group_name="gpu_tracker",
    kinds={"polars", "duckdb"},
    io_manager_key=IOManager.DUCKDB.value,
    metadata={"schema": dbt_project.name},
)
async def gpu_tracker__datablitz_raw(context: dg.AssetExecutionContext):
    async with open(
        settings.BASE_DIR / "src/assets/gpu_tracker/datablitz_products.graphql"
    ) as f:
        query = await f.read()

    page = 1
    limit = 250
    cursor = None
    products = []
    has_next_page = False

    async with AsyncSession(
        base_url="https://datablitz-inc.myshopify.com",
        allow_redirects=True,
        impersonate="chrome",
    ) as session:
        while True:
            context.log.info(f"🔨 Fetching page {page=:,}...")
            res = await session.post(
                "/api/2025-10/graphql.json",
                json={
                    "query": query,
                    "variables": {
                        "first": limit,
                        "after": cursor,
                    },
                },
            )
            data = res.json()

            if data.get("data", {}).get("products", {}).get("edges") is None:
                context.log.error("❌ `edges` key not found in response")
                break

            _products = data["data"]["products"]["edges"]
            has_next_page = data["data"]["products"]["pageInfo"].get(
                "hasNextPage", False
            )
            if len(_products) == 0 or not has_next_page:
                context.log.info(
                    f"✅ No more products found, total {len(products):,} products"
                )
                break

            products.extend(_products)
            context.log.info(
                f"☑️ Fetched {len(_products):,} products, total {len(products):,} products"
            )
            cursor = data["data"]["products"]["pageInfo"].get("endCursor", None)
            page += 1

            base_delay = random.randint(1, 3)
            jitter = random.uniform(0, 1)
            delay = base_delay + jitter
            context.log.info(f"⌛ Sleeping for {delay:.2f} seconds...")
            await sleep(delay)

    df = pl.from_dicts(products).with_columns(
        retrieved_at=pl.lit(datetime.now(ZoneInfo("UTC"))),
    )
    context.add_output_metadata({"dagster/row_count": len(df)})
    return df
