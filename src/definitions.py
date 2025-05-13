from dagster import Definitions, load_assets_from_package_module
from dagster.components import load_defs

import src.defs
from src.assets import dbt as dbt_assets
from src.assets.cchain.factory import (
    CCHAIN_DATASETS,
    UPSTREAM_KEYS as CCHAIN_UPSTREAM_KEYS,
    build_cchain_delta_asset,
    build_cchain_raw_asset,
)
from src.assets.nasa_firms.factory import (
    SATELLITE_CODES,
    UPSTREAM_KEYS as NASA_FIRMS_UPSTREAM_KEYS,
    build_viirs_delta_asset,
    build_viirs_raw_asset,
)
from src.resources import RESOURCES
from src.sensors import latest_er_batch_sensor

defs = Definitions.merge(
    *[build_cchain_raw_asset(dataset) for dataset in CCHAIN_DATASETS],
    *[build_cchain_delta_asset(key) for key in CCHAIN_UPSTREAM_KEYS],
    *[build_viirs_raw_asset(code) for code in SATELLITE_CODES],
    *[build_viirs_delta_asset(key) for key in NASA_FIRMS_UPSTREAM_KEYS],
    Definitions(
        assets=[
            *load_assets_from_package_module(dbt_assets),
        ],
        resources=RESOURCES,
        sensors=[latest_er_batch_sensor],
    ),
    load_defs(defs_root=src.defs),
)
