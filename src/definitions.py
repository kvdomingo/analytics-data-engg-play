from dagster import Definitions, load_assets_from_package_module

from src.assets import cchain, fires
from src.assets.cchain.factory import CCHAIN_DATASETS, build_cchain_raw_asset
from src.resources import RESOURCES

defs = Definitions.merge(
    *[build_cchain_raw_asset(dataset) for dataset in CCHAIN_DATASETS],
    Definitions(
        assets=[
            *load_assets_from_package_module(cchain, "cchain"),
            *load_assets_from_package_module(fires, "fires"),
        ],
        resources=RESOURCES,
    ),
)
