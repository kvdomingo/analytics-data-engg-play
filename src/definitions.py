from dagster import Definitions, load_assets_from_package_module

from src import assets
from src.resources import RESOURCES

defs = Definitions(
    assets=[*load_assets_from_package_module(assets)],
    resources=RESOURCES,
)
