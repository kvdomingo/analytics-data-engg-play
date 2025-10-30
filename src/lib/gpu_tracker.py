import random
from asyncio import sleep
from typing import Any

from curl_cffi import AsyncSession
from dagster import AssetExecutionContext

SHOPIFY_PAGE_LIMIT = 250


async def crawl_shopify_products_json(
    context: AssetExecutionContext,
    base_url: str,
    path: str,
    extra_params: dict[str, Any],
) -> list[dict[str, Any]]:
    page = 1
    products = []

    async with AsyncSession(
        base_url=base_url,
        allow_redirects=True,
        impersonate="chrome",
    ) as session:
        while True:
            context.log.info(f"Fetching {page=:,}...")

            # Access Shopify products.json directly
            res = await session.get(
                path,
                params={
                    **extra_params,
                    "page": page,
                    "limit": SHOPIFY_PAGE_LIMIT,
                },
            )
            data = res.json()

            if data.get("products") is None:
                context.log.error("`products` key not found in response")
                break

            _products = data["products"]
            if len(_products) == 0:
                context.log.info(
                    f"No more products found, total {len(products):,} products"
                )
                break

            products.extend(_products)
            context.log.info(
                f"Fetched {len(_products):,} products from {page=:,}, total {len(products):,} products"
            )
            page += 1

            base_delay = random.randint(1, 3)
            jitter = random.uniform(0, 1)
            delay = base_delay + jitter
            await sleep(delay)

    return products
