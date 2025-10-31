import random
from asyncio import sleep
from datetime import datetime
from zoneinfo import ZoneInfo

import dagster as dg
import polars as pl
from aiofiles import open
from curl_cffi import AsyncSession
from dagster_duckdb import DuckDBResource

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


@dg.asset(
    group_name="gpu_tracker",
    kinds={"duckdb", "postgres"},
    deps=["gpu_tracker__products", "gpu_tracker__variants"],
)
async def gpu_tracker__postgres_copy(duckdb: DuckDBResource) -> None:
    with duckdb.get_connection() as conn:
        conn.install_extension("postgres")
        conn.load_extension("postgres")

        conn.execute(f"""
        CREATE SECRET (
            TYPE postgres,
            HOST '{settings.GPU_TRACKER_POSTGRES_HOST}',
            PORT '{settings.GPU_TRACKER_POSTGRES_PORT}',
            DATABASE '{settings.GPU_TRACKER_POSTGRES_DATABASE}',
            USER '{settings.GPU_TRACKER_POSTGRES_USERNAME.get_secret_value()}',
            PASSWORD '{settings.GPU_TRACKER_POSTGRES_PASSWORD.get_secret_value()}'
        );

        ATTACH '' AS pg (TYPE postgres);
        """)
        conn.execute("""
        BEGIN TRANSACTION;

        DROP TABLE IF EXISTS pg.variants;
        DROP TABLE IF EXISTS pg.products;

        CREATE TABLE pg.public.products AS
        SELECT * FROM ae_de_play.gpu_tracker__products;

        CREATE TABLE pg.public.variants AS
        SELECT * FROM ae_de_play.gpu_tracker__variants;

        COMMIT;
        """)
        conn.execute("""
        SELECT * FROM postgres_execute(
            'pg',
            '
                ALTER TABLE products
                ADD CONSTRAINT products_pk PRIMARY KEY (id);

                ALTER TABLE variants
                ADD CONSTRAINT variants_pk PRIMARY KEY (id),
                ADD CONSTRAINT variants_product_id_fk FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE;
            '
        );
        """)
