from dagster import Definitions

from src.assets.cchain.factory import CCHAIN_DATASETS, build_cchain_raw_asset
from src.assets.dbt.assets import dbt_assets
from src.assets.nasa_firms.factory import SATELLITE_CODES, build_viirs_raw_asset
from src.resources import RESOURCES

defs = Definitions.merge(
    *[build_cchain_raw_asset(dataset) for dataset in CCHAIN_DATASETS],
    *[build_viirs_raw_asset(code) for code in SATELLITE_CODES],
    Definitions(
        assets=[dbt_assets],
        resources=RESOURCES,
    ),
)
