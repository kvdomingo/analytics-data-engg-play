from dagster import Definitions, load_assets_from_package_module
from dagster.components import load_defs

import src.defs
from src.assets import dbt as dbt_assets
from src.assets.cchain.factory import CCHAIN_DATASETS, build_cchain_raw_asset
from src.assets.nasa_firms.factory import (
    SATELLITE_CODES,
    UPSTREAM_KEYS,
    build_viirs_delta_asset,
    build_viirs_raw_asset,
)
from src.resources import RESOURCES

defs = Definitions.merge(
    *[build_cchain_raw_asset(dataset) for dataset in CCHAIN_DATASETS],
    *[build_viirs_raw_asset(code) for code in SATELLITE_CODES],
    *[build_viirs_delta_asset(key) for key in UPSTREAM_KEYS],
    Definitions(
        assets=[
            *load_assets_from_package_module(dbt_assets),
        ],
        resources=RESOURCES,
    ),
    load_defs(defs_root=src.defs),
)
